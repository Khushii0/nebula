/// <reference types="react-scripts" />

declare module 'react-canvas-draw' {
  import { Component } from 'react';
  
  export interface CanvasDrawProps {
    ref?: React.Ref<CanvasDraw>;
    brushColor?: string;
    brushRadius?: number;
    lazyRadius?: number;
    canvasWidth?: number;
    canvasHeight?: number;
    style?: React.CSSProperties;
    saveData?: string;
    immediateLoading?: boolean;
    hideInterface?: boolean;
    gridColor?: string;
    backgroundColor?: string;
    onChange?: (canvas: CanvasDraw) => void;
    loadTimeOffset?: number;
  }
  
  export default class CanvasDraw extends Component<CanvasDrawProps> {
    clear(): void;
    undo(): void;
    getSaveData(): string;
    loadSaveData(saveData: string, immediate?: boolean): void;
  }
}