import { NavLink } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

function NavBar() {
  const { user, logout } = useAuth();

  return (
    <nav>
      {user ? (
        <div>
          <NavLink label="Home" to="/" >Home</NavLink>
          <NavLink label="Profile" to="/profile" >Profile</NavLink>
        </div>
      ) : (
        <div>
          <NavLink label="Home" to="/" >Home</NavLink>
          <NavLink label="Login" to="/login">Login</NavLink>
          <NavLink label="Signup" to="/signup">Signup</NavLink>
        </div>
      )}
    </nav>
  )
}

export default NavBar;