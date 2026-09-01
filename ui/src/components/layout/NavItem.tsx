import { NavLink, NavLinkProps } from "react-router-dom";

/**
 * Sidebar navigation item styled for the genomics console.
 */
export function NavItem({ children, ...props }: NavLinkProps) {
  return (
    <NavLink
      {...props}
      className={({ isActive }) =>
        `flex items-center gap-2.5 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
          isActive
            ? "bg-accent/15 text-accent"
            : "text-fg-dim hover:bg-surface-2 hover:text-fg"
        }`
      }
    >
      {children}
    </NavLink>
  );
}
