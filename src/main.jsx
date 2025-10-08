import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import Root from "./Root";
import { ThemeProvider } from './context/ThemeContext';

const root = createRoot(document.getElementById("root"));  // ✅ use createRoot here
root.render(
  <StrictMode>
    <ThemeProvider>
      <Root />
    </ThemeProvider>
  </StrictMode>
);
