import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { getEvent, updateEvent, deleteEvent } from "../services/eventService"
import { listEventTournaments } from "../services/tournamentService";
import TournamentListItem from "../components/tournamentitem/TournamentListItem";
import DateTimePicker from "../components/DateTimePicker"

// Public Page (Read-only)
// If owner of the event or admin, Inline PATCH/DEL
function EventDetails() {
  const { eventId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [event, setEvent] = useState(null)
  const [tournaments, setTournaments] = useState([])
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  // Edit + Delete (owner or admin)
  const [isEditing, setIsEditing] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    start: new Date(),
    end: new Date(),
    in_person: false,
    location: '',
    description: '',
    tie_breaking_rule: ''
  })

  // Retrieve events and list event tournaments (read)
  useEffect( () => {
    Promise.all([getEvent(eventId), listEventTournaments(eventId)])
      .then(([fetchedEvent, fetchedTournaments]) => {
        setEvent(fetchedEvent)
        setTournaments(fetchedTournaments)
      })
      .catch((err) => setError(err.message || 'Unable to load event details'))
      .finally(()=> setIsLoading(false))
  }, [eventId])

  // Edit + Delete (owner or admin)
  const isOwner = Boolean(event && user && event.host_id === user.id)
  const isAdmin = Boolean(event && user?.roles?.some(userRole => userRole.role?.name === "admin"))

  function addTournament() {navigate(`/events/${eventId}/tournaments/create`)}

  function startEditing() {
    setFormData({
      name: event.name,
      start: event.start,
      end: event.end,
      in_person: event.in_person,
      location: event.location,
      description: event.description,
      tie_breaking_rule: event.tie_breaking_rule
    })
    setIsEditing(true)
  }

  function handleChange(e) {setFormData({...formData, [e.target.name]: e.target.value})}
  
  async function handleSave(e) {
    setIsSubmitting(true)
    try {
      const updated = await updateEvent(eventId, formData)
      setEvent(updated)
    } catch (err) {
      setError(err.message || 'Unable to update event')
    } finally {
      setIsEditing(false)
      setIsSubmitting(false)
    }
  }

  async function handleDelete(e) {
    setIsSubmitting(true)
    try {
      await deleteEvent(eventId)
      navigate('/')
    } catch (err) {
      setError(err.message || 'Unable to delete event')
      setIsSubmitting(false)
    }
  }

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!event) return <p>Event not found.</p>;

  return (
    <>
      <div className="event-header-details-container">
        {isEditing ? (
          <>
            <input
              name="name"
              value={formData.name}
              onChange={handleChange}
            />
            <input
              name="start"
              value={formData.start}
              onChange={handleChange}
            />
            <input
              name="location"
              value={formData.location}
              onChange={handleChange}
            />
            <button onClick={handleSave} disabled={isSubmitting}>
              {isSubmitting ? 'Saving...' : 'Save'}
            </button>
            <button onClick={() => setIsEditing(false)}>Cancel</button>
          </>
        ) : (
          <>
            <h2>{event.name}</h2>
            <h3>{event.start}</h3>
            <h3>{event.location}</h3>
            {(isOwner || isAdmin) && (
              <>
                <button onClick={addTournament}>Add Tournament to Event</button>
                <button onClick={startEditing}>Edit</button>
                <button onClick={handleDelete}>
                  {isSubmitting ? 'Deleting...' : 'Delete'}
                </button>
              </>
            )}
          </>
        )}
      </div>

      <div className="event-tournaments-items-container">
        <ul>
          <li>
            {tournaments.map((tournament) => (
              <TournamentListItem
                key={tournament.id}
                event={event}
                tournament={tournament}
              />
            ))} 
          </li>
        </ul>
      </div>

      <div className="event-FAQ-container">
        {isEditing ? (
          <>
            <label>
              Start
              <DateTimePicker
                name="name"
                value={formData.start}
                onChange={(dt)=> setFormData({...formData, start: dt})}
              />
            </label>
            <label>
              End
              <DateTimePicker
                name="end"
                value={formData.end}
                onChange={(dt)=> setFormData({...formData, end: dt})}
              />
            </label>
            <label>
              Location
              <input
                name="location"
                value={formData.location}
                onChange={handleChange}
              />
            </label>
            <label>
              Description
              <input
                name="description"
                value={formData.description}
                onChange={handleChange}
              />
            </label>
            <label>
              Rules
              <input
                name="tie_breaking_rule"
                value={formData.tie_breaking_rule}
                onChange={handleChange}
              />
            </label>
          </>
        ) : (
          <>
            <h2>FAQ</h2>
            <h3>Start:  </h3>
            <p>{event.start}</p>
            <h3>End:  </h3>
            <p>{event.end}</p>
            <h3>Location:  </h3>
            <p>{event.location}</p>
            <h3>Description:  </h3>
            <p>{event.description}</p>
            {event.tie_breaking_rule ? (
              <>
                <h3>Rules: </h3>
                <p>{event.tie_breaking_rule}</p>
              </>
            ) : (
              null
            )}
          </>
        )}
      </div>
    </>
  )
}

export default EventDetails;