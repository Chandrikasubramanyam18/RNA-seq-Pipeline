import type { ReactNode } from "react";

interface TabsProps<T extends string> {
  tabs: { key: T; label: string }[];
  active: T;
  onChange: (key: T) => void;
}

export function Tabs<T extends string>({ tabs, active, onChange }: TabsProps<T>) {
  return (
    <div className="flex gap-1 border-b border-border">
      {tabs.map((tab) => (
        <button
          key={tab.key}
          onClick={() => onChange(tab.key)}
          className={`px-3 py-2 text-sm font-medium transition-colors ${
            active === tab.key
              ? "border-b-2 border-accent text-accent"
              : "border-b-2 border-transparent text-fg-dim hover:text-fg"
          }`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}

export interface StepResult<T extends string> {
  key: T;
  content: ReactNode;
}
