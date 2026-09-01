import type { ReactNode } from "react";
import { Loading } from "@/components/common/Loading";
import { ErrorState } from "@/components/common/ErrorState";

interface ResolvedProps {
  loading: boolean;
  error: Error | null;
  children: ReactNode;
}

/** Renders loading / error / children based on query state. */
export function Resolved({ loading, error, children }: ResolvedProps) {
  if (loading) return <Loading />;
  if (error) return <ErrorState message={error.message} />;
  return <>{children}</>;
}
