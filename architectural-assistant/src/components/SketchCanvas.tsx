import React, { useRef, useEffect } from "react";
// @ts-ignore - react-canvas-draw doesn't have types
import CanvasDraw from "react-canvas-draw";
import axios from "axios";

interface SketchCanvasProps {
  projectId: string;
  canvasRef?: React.MutableRefObject<any>;
}

const SketchCanvas: React.FC<SketchCanvasProps> = ({ projectId, canvasRef: externalRef }) => {
  const internalRef = useRef<any>(null);
  
  // Sync internal ref with external ref if provided
  useEffect(() => {
    if (externalRef && internalRef.current) {
      externalRef.current = internalRef.current;
    }
  }, [externalRef]);
  
  const canvasRef = externalRef || internalRef;

  const handleSave = async () => {
    if (!canvasRef.current) return;
    const sketchData = canvasRef.current.getSaveData();

    try {
      await axios.post(`/projects/${projectId}/sketch`, { sketch: sketchData });
      alert("Sketch saved successfully!");
    } catch (err) {
      console.error(err);
      alert("Failed to save sketch.");
    }
  };

  const handleClear = () => {
    canvasRef.current?.clear();
  };

  return (
    <div style={{ border: "1px solid #ccc", borderRadius: "5px", padding: "10px", background: "white" }}>
      <CanvasDraw
        ref={canvasRef}
        brushColor="#000"
        brushRadius={2}
        lazyRadius={0}
        canvasWidth={600}
        canvasHeight={400}
        style={{ border: "1px solid #ddd" }}
      />
      <div style={{ marginTop: "10px", display: "flex", gap: "10px" }}>
        <button onClick={handleSave} style={{ padding: "5px 15px" }}>Save Sketch</button>
        <button onClick={handleClear} style={{ padding: "5px 15px" }}>Clear</button>
      </div>
    </div>
  );
};

export default SketchCanvas;
