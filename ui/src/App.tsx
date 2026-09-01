import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { DashboardPage } from "@/pages/DashboardPage";
import { ProjectsPage } from "@/pages/ProjectsPage";
import { ProjectDetailPage } from "@/pages/ProjectDetailPage";
import { QcPage } from "@/pages/QcPage";
import { AlignmentPage } from "@/pages/AlignmentPage";
import { ExpressionPage } from "@/pages/ExpressionPage";
import { DifferentialExpressionPage } from "@/pages/DifferentialExpressionPage";
import { PathwaysPage } from "@/pages/PathwaysPage";
import { ReportsPage } from "@/pages/ReportsPage";

export default function App() {
  return (
    <BrowserRouter>
      <AppLayout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/projects" element={<ProjectsPage />} />
          <Route path="/projects/:id" element={<ProjectDetailPage />} />
          <Route path="/qc" element={<QcPage />} />
          <Route path="/alignment" element={<AlignmentPage />} />
          <Route path="/expression" element={<ExpressionPage />} />
          <Route path="/differential-expression" element={<DifferentialExpressionPage />} />
          <Route path="/pathways" element={<PathwaysPage />} />
          <Route path="/reports" element={<ReportsPage />} />
        </Routes>
      </AppLayout>
    </BrowserRouter>
  );
}
