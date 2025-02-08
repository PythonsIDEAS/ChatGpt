import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App"; // Import your App component
import "./index.css"; // Import global styles (e.g., TailwindCSS or custom CSS)

const root = ReactDOM.createRoot(document.getElementById("root")); // Get the root element

root.render(
  <React.StrictMode>
    <App /> {/* Render the App component */}
  </React.StrictMode>
);
