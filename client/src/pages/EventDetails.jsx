import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { getEvent } from "../services/eventService"
import { listEventTournaments } from "../services/tournamentService";
import TournamentListItem from "../components/tournamentitem/TournamentListItem";

// Public (Read-only)
// If owner of the event or admin, POST/PATCH/DEL

function EventDetails() {
  const { eventId } = useParams();
  const { user } = useAuth();
  const [event, setEvent] = useState(null)
  const [tournaments, setTournaments] = useState([])
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect( () => {
    Promise.all([getEvent(eventId), listEventTournaments(eventId)])
      .then(([fetchedEvent, fetchedTournaments]) => {
        setEvent(fetchedEvent)
        setTournaments(fetchedTournaments)
      })
      .catch((err) => setError(err.message || 'unable to load'))
      .finally(()=> setIsLoading(false))
  }, [eventId])

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!event) return <p>Event not found.</p>;

  return (
    <>
      <div className="event-header-details-container">
        <h2>{event.name}</h2>
        <h3>{event.start}</h3>
        <h3>{event.location}</h3>
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
        <h2>FAQ</h2>
        <h3>Start:  </h3>
        <p>{event.start}</p>
        <h3>End:  </h3>
        <p>{event.end}</p>
        <h3>Location:  </h3>
        <p>{event.location}</p>
        <h3>Description:  </h3>
        <p>{event.description}</p>
        <h3>Rules: </h3>
        <p>{event.tie_breaking_rule}</p>
      </div>
    </>
  )
}

export default EventDetails;