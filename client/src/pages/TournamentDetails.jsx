import { useState } from "react";
import { useParams, useNavigate, useOutletContext, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { updateEventTournament, deleteEventTournament } from "../services/tournamentService";
import CompetitorRow from "../components/competitors/CompetitorRow";
import DateTimePicker from "../components/DateTimePicker";

// Public Page. GET and POST (register) to tournament
// If owner of the event or admin, Inline PATCH/DEL
function TournamentDetails() {
  const { eventId, tournamentId } = useParams();
  const { user } = useAuth();
  const { event } = useOutletContext()
  const [tournamentDetails, setTournamentDetails] = useState(event.tournaments.find((t) => String(t.id) === String(tournamentId)) || null)
  const navigate = useNavigate();
  
  // Edit + Delete if owner or admin
  const [isEditing, setIsEditing] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    name: '',
    start_time: new Date(),
    registration_deadline: new Date(),
    game: '',
    platform: '',
    line_up_type: ''
  })

  const isOwner = Boolean(tournamentDetails && user && event.host_id === user.id)
  const isAdmin = Boolean(tournamentDetails && user?.roles?.some(userRole => userRole.role?.name === "admin"))

  // Navigate to Register page or Signup Page depending on Authenticated User
  function handleRegister() {
    { user ? (
      navigate(`/events/${eventId}/tournaments/${tournamentId}/register`)
    ): (
      navigate('/signup')
    )}
  }

  // Inline Editing
  function startEditing() {
    setForm({
    name: tournamentDetails.name,
    start_time: tournamentDetails.start_time,
    registration_deadline: tournamentDetails.registration_deadline,
    game: tournamentDetails.game,
    platform: tournamentDetails.platform,
    line_up_type: tournamentDetails.line_up_type
    })
    setIsEditing(true)
  }

  // Update
  async function handleSave(e) {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      const updated = await updateEventTournament(eventId, tournamentId, form)
      setTournamentDetails(updated)
      setIsEditing(false)
    } catch (err) {
      setError(err.message || 'Unable to update tournament')
    } finally {
      setIsSubmitting(false)
    }
  }

  // Delete
  async function handleDelete(e) {
    setError('')
    setIsSubmitting(true)
    try {
      await deleteEventTournament(eventId, tournamentId)
      navigate(`/events/${eventId}`)
    } catch (err) {
      setError(err.message || 'Unable to delete tournament')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (!tournamentDetails) return <p>Tournament Details not found</p>

  return (
    <>
      <div className="tournament-header-details-container">
        { isEditing ? (
          <>
            <label>Name:</label>
            <input
              name="name"
              value={form.name}
              onChange={(e)=> setForm({...form, name: e.target.value})}
            />
            <label>Line Up Type:</label>
            <input
              name="line_up_type"
              value={form.line_up_type}
              onChange={(e)=> setForm({...form, line_up_type: e.target.value})}
            />
            <label>Game:</label>
            <input
              name="game"
              value={form.game}
              onChange={(e)=> setForm({...form, game: e.target.value})}
            />
            <label>Platform:</label>
            <input
              name="platform"
              value={form.platform}
              onChange={(e)=> setForm({...form, platform: e.target.value})}
            />
            <label>Start Time:</label>
            <DateTimePicker
              name="start_time"
              value={form.start_time}
              onChange={(dt)=> setForm({...form, start_time: dt})}
            />
            <button onClick={handleSave} disabled={isSubmitting}>
              {isSubmitting ? 'Saving...' : 'Save'}  
            </button>
            <button onClick={() => setIsEditing(false)}>Cancel</button>
            {error && <p role="alert">{error}</p>}
          </>
        ) : (
          <>
            <h2>{tournamentDetails.name} -- {event.name}</h2>
            <h3>{tournamentDetails.line_up_type}--{tournamentDetails.game}--{tournamentDetails.platform}</h3>
            <h3>{tournamentDetails.start_time}</h3>
            {(isOwner || isAdmin) && (
              <>
                <button onClick={startEditing}>Edit</button>
                <button onClick={handleDelete}>Delete</button>
                {error && <p role="alert">{error}</p>}
              </>
            )}
          </>
        )}
      </div>

      <div className="tournament-registration-container">
        {isEditing ? (
          <>
            <label>Deadline to register:</label>
            <DateTimePicker
              name="registration_deadline"
              value={form.registration_deadline}
              onChange={(dt)=> setForm({...form, registration_deadline: dt})}
            />
          </>
        ) : (
          <>
            <h2>Register now!</h2>
            <h3>Deadline: {tournamentDetails.registration_deadline}</h3>
            <button onClick={handleRegister}>Register</button>
          </>
        )}
      </div>

      <div className="tournament-attendee-list-container">
        <h2>Competitors:</h2>
        {tournamentDetails.competitors.map((competitor) => (
          <CompetitorRow
            key={competitor.id}
            competitor={competitor}
          />
        ))}
      </div>

      <div className="tournament-matches-container">
        <Link to={`/events/${eventId}/tournaments/${tournamentId}/matches`}><h2>Matches</h2></Link>
      </div>

      <div className="tournament-standings-container">
        <Link to={`/events/${eventId}/tournaments/${tournamentId}/standings`}><h2>Standings</h2></Link>
      </div>

      <div className="tournament-bracket-container">
        <Link to={`/events/${eventId}/tournaments/${tournamentId}/bracket`}><h2>Bracket</h2></Link>
      </div>
    </>
  )
}

export default TournamentDetails;