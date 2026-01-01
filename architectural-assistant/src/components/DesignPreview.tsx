import React from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

interface DesignPreviewProps {
  modelUrl?: string; // Optional URL to load real 3D model from backend
}

const DesignPreview: React.FC<DesignPreviewProps> = ({ modelUrl }) => {
  return (
    <div style={{ border: "1px solid #ccc", borderRadius: "5px", padding: "10px", background: "white", height: "400px" }}>
      <Canvas style={{ height: "100%", width: "100%" }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <directionalLight position={[0, 10, 5]} intensity={1} />
        <OrbitControls />
        {/* Placeholder: simple box. Replace with loaded model when modelUrl is available */}
        <mesh position={[0, 0, 0]}>
          <boxGeometry args={[2, 2, 2]} />
          <meshStandardMaterial color="orange" />
        </mesh>
        {/* Grid helper for reference */}
        <gridHelper args={[10, 10]} />
      </Canvas>
    </div>
  );
};

export default DesignPreview;
