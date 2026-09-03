import { Routes, Route } from "react-router-dom"
// Pages
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Profile from "./pages/Profile";
import Unauthorized from "./pages/Unauthorized";
import CreateEvent from "./pages/CreateEvent";
import EventDetails from "./pages/EventDetails";
import TournamentDetails from "./pages/TournamentDetails";
import Matches from "./pages/Matches";
import Standings from "./pages/Standings";
import Bracket from "./pages/Bracket";
import NotFound from "./pages/NotFound";

// Components
import NavBar from './components/NavBar'
import Footer from './components/Footer'
import ProtectedRoute from "./components/ProtectedRoute";
import RequireRole from "./components/RequireRole";

function App() {

  return (
    <>
      <NavBar/>

      {/* Public Routes */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/unauthorized" element={<Unauthorized />} />

        {/* Protected - any authenticated user */}
        <Route element={<ProtectedRoute/>}>
          <Route path="/profile" element={<Profile />} />
        </Route>

        {/* Host or admin */}
        <Route element={<RequireRole roles={["host", "admin"]} />}>
          <Route path="/events/create" element={<CreateEvent /> } />
        </Route>

        {/* Public event/tournament pages */}
        <Route path="/events/:eventId" element={<EventDetails />} />
        <Route path="/events/:eventId/tournaments/:tournamentId" element={<TournamentDetails />} />
        <Route path="/events/:eventId/tournaments/:tournamentId/matches" element={<Matches />} />
        <Route path="/events/:eventId/tournaments/:tournamentId/matches" element={<Standings />} />
        <Route path="/events/:eventId/tournaments/:tournamentId/matches" element={<Bracket />} />

        <Route path="*" element={<NotFound/> }/>
      </Routes>

      <Footer/>
    </>
  )
}

export default App;
