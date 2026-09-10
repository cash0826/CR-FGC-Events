import { NavLink } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import logo from "../assets/logo.png";

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
    <nav className="navbar-container">

      {/* Logo */}
      <a className="navbar-brand-logo" href="/">
        <img src={logo}></img>
      </a>

      {/* Navbar Toggler */}
      <button className="navbar-toggler" type="button" aria-controls="navbarLinks" aria-expanded="false">
        <span className="icon-bar"></span>
        <span className="icon-bar"></span>
        <span className="icon-bar"></span>
      </button>

      {/* Nav Links & Join Now button (collapsed on narrow screen) */}
      <div id="#navbarLinks" className="collapse navbar-links-center-container">
      {user ? (
        <>
          <NavLink label="Home" to="/" >Home</NavLink>
          <NavLink label="Profile" to="/profile" >Profile</NavLink>
          {getCreateEvent()}
        </>
      ) : (
        <>
          <NavLink label="Home" to="/" >Home</NavLink>
          <NavLink label="Login" to="/login">Login</NavLink>
          <NavLink label="Signup" to="/signup">Signup</NavLink>
        </>
      )}
      </div>
    </nav>
  )
}

export default NavBar;