import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

function RequireRole({ roles }) {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (!user?.roles) {
    return <Navigate to="/unauthorized" replace />;
  }

  const hasRole = roles.some(role => user.roles.includes(role));

  if (!hasRole) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <Outlet />;
}

export default RequireRole;