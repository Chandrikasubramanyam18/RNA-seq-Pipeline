import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { QueryProvider } from "@/hooks/QueryProvider";
import App from "@/App";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <QueryProvider>
      <App />
    </QueryProvider>
  </React.StrictMode>
);
