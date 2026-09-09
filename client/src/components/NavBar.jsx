import { NavLink } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

function NavBar() {
  const { user } = useAuth();
  const roles = ["admin", "host"]  

  function getCreateEvent() {
    if (user) {
      const hasRole = user.roles.some(userRole => roles.includes(userRole.role?.name))
      return hasRole ? <NavLink label="Create_Event" to="/events/create">Create Event</NavLink> : null
    }
  }

  return (
    <nav>
      {user ? (
        <div>
          <NavLink label="Home" to="/" >Home</NavLink>
          <NavLink label="Profile" to="/profile" >Profile</NavLink>
          {getCreateEvent()}
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