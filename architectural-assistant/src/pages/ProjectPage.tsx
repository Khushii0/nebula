import React, { useState, useEffect, useRef } from "react";
import SketchCanvas from "../components/SketchCanvas";
import DesignPreview from "../components/DesignPreview";
import axios from "axios";

interface Project {
  id: number;
  title: string;
  description: string;
  design_narrative?: string;
  compliance_notes?: string;
  design_concept_url?: string;
}

const ProjectPage: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [textBrief, setTextBrief] = useState("");
  const [designData, setDesignData] = useState<any>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [newProjectTitle, setNewProjectTitle] = useState("");
  const [newProjectDesc, setNewProjectDesc] = useState("");
  const [showNewProject, setShowNewProject] = useState(false);
  const canvasRef = useRef<any>(null);

  useEffect(() => {
    loadProjects();
  }, []);

  useEffect(() => {
    if (selectedProject) {
      setTextBrief(selectedProject.description || "");
      if (selectedProject.design_narrative) {
        setDesignData({
          design_narrative: selectedProject.design_narrative,
          compliance_notes: selectedProject.compliance_notes,
          design_concept_url: selectedProject.design_concept_url,
        });
      }
    }
  }, [selectedProject]);

  const loadProjects = async () => {
    try {
      const res = await axios.get("/projects/");
      setProjects(res.data);
      if (res.data.length > 0 && !selectedProject) {
        setSelectedProject(res.data[0]);
      }
    } catch (err: any) {
      console.error("Failed to load projects:", err);
      if (err.code === 'ERR_NETWORK') {
        alert('Cannot connect to backend. Make sure backend is running on http://localhost:8000');
      } else if (err.response?.status === 401) {
        // Token expired, redirect to login
        window.location.reload();
      }
    }
  };

  const createProject = async () => {
    if (!newProjectTitle.trim()) {
      alert("Please enter a project title");
      return;
    }
    try {
      const res = await axios.post("/projects/", {
        title: newProjectTitle,
        description: newProjectDesc,
      });
      setProjects([...projects, res.data]);
      setSelectedProject(res.data);
      setNewProjectTitle("");
      setNewProjectDesc("");
      setShowNewProject(false);
    } catch (err) {
      console.error("Failed to create project:", err);
      alert("Failed to create project");
    }
  };

  const handleGenerateDesign = async () => {
    if (!selectedProject) {
      alert("Please select or create a project first");
      return;
    }
    if (!textBrief.trim()) {
      alert("Please enter a design brief");
      return;
    }

    setIsGenerating(true);
    try {
      // Get sketch data from canvas
      let sketchData = null;
      if (canvasRef.current && typeof canvasRef.current.getSaveData === 'function') {
        try {
          sketchData = canvasRef.current.getSaveData();
        } catch (err) {
          console.warn("Could not get sketch data:", err);
        }
      }

      const formData = new FormData();
      formData.append("project_id", selectedProject.id.toString());
      formData.append("text_brief", textBrief);
      if (sketchData) {
        formData.append("sketch_data", sketchData);
      }

      const res = await axios.post("/ai/generate_design/form", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setDesignData(res.data);
      
      // Update project with new data
      await axios.put(`/projects/${selectedProject.id}`, {
        description: textBrief,
        sketch_data: sketchData,
        design_narrative: res.data.design_narrative,
        compliance_notes: res.data.compliance_notes,
        design_concept_url: res.data.design_concept_url,
      });

      // Reload projects to get updated data
      loadProjects();
    } catch (err: any) {
      console.error("Failed to generate design:", err);
      if (err.code === 'ERR_NETWORK') {
        alert('Cannot connect to backend. Make sure backend is running on http://localhost:8000');
      } else if (err.response?.status === 401) {
        alert('Session expired. Please login again.');
        window.location.reload();
      } else {
        alert(err.response?.data?.detail || "Failed to generate design");
      }
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div style={{ padding: "20px", display: "flex", gap: "20px", height: "calc(100vh - 80px)" }}>
      {/* Sidebar */}
      <div style={{ width: "250px", borderRight: "1px solid #ccc", paddingRight: "20px" }}>
        <h2>Projects</h2>
        <button
          onClick={() => setShowNewProject(!showNewProject)}
          style={{ marginBottom: "10px", width: "100%" }}
        >
          {showNewProject ? "Cancel" : "+ New Project"}
        </button>
        
        {showNewProject && (
          <div style={{ marginBottom: "20px", padding: "10px", background: "#f5f5f5", borderRadius: "5px" }}>
            <input
              type="text"
              placeholder="Project Title"
              value={newProjectTitle}
              onChange={(e) => setNewProjectTitle(e.target.value)}
              style={{ width: "100%", marginBottom: "5px", padding: "5px" }}
            />
            <textarea
              placeholder="Description"
              value={newProjectDesc}
              onChange={(e) => setNewProjectDesc(e.target.value)}
              style={{ width: "100%", marginBottom: "5px", padding: "5px", minHeight: "60px" }}
            />
            <button onClick={createProject} style={{ width: "100%" }}>
              Create
            </button>
          </div>
        )}

        <div style={{ display: "flex", flexDirection: "column", gap: "5px" }}>
          {projects.map((project) => (
            <button
              key={project.id}
              onClick={() => setSelectedProject(project)}
              style={{
                padding: "10px",
                textAlign: "left",
                background: selectedProject?.id === project.id ? "#e0e0e0" : "white",
                border: "1px solid #ccc",
                cursor: "pointer",
              }}
            >
              {project.title}
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "20px" }}>
        {selectedProject ? (
          <>
            <div>
              <h2>{selectedProject.title}</h2>
              <textarea
                placeholder="Enter design brief here..."
                value={textBrief}
                onChange={(e) => setTextBrief(e.target.value)}
                style={{
                  width: "100%",
                  height: "100px",
                  padding: "10px",
                  marginBottom: "10px",
                  fontSize: "14px",
                }}
              />
              <button
                onClick={handleGenerateDesign}
                disabled={isGenerating}
                style={{
                  padding: "10px 20px",
                  fontSize: "16px",
                  background: "#4CAF50",
                  color: "white",
                  border: "none",
                  borderRadius: "5px",
                  cursor: isGenerating ? "not-allowed" : "pointer",
                }}
              >
                {isGenerating ? "Generating..." : "Generate Design"}
              </button>
            </div>

            <div style={{ display: "flex", gap: "20px", flex: 1, minHeight: 0 }}>
              <div style={{ flex: 1 }}>
                <h3>Sketch Canvas</h3>
                <SketchCanvas projectId={selectedProject.id.toString()} canvasRef={canvasRef} />
              </div>
              <div style={{ flex: 1 }}>
                <h3>3D Preview</h3>
                <DesignPreview modelUrl={designData?.design_concept_url} />
              </div>
            </div>

            {designData && (
              <div style={{ marginTop: "20px", padding: "20px", background: "#f9f9f9", borderRadius: "5px" }}>
                <h3>Design Narrative</h3>
                <p style={{ whiteSpace: "pre-wrap" }}>{designData.design_narrative}</p>
                <h3 style={{ marginTop: "20px" }}>Compliance Notes</h3>
                <p style={{ whiteSpace: "pre-wrap" }}>{designData.compliance_notes}</p>
              </div>
            )}
          </>
        ) : (
          <div>
            <p>Create a new project to get started</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectPage;
