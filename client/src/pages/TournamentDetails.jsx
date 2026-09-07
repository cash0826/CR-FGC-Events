import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { getTournament } from "../services/tournamentService";
import CompetitorRow from "../components/competitors/CompetitorRow";

// Public (Read and register to tournament)
// If event owner or admin, POST/PATCH/DEL

function TournamentDetails() {
  const { eventId, tournamentId } = useParams();
  const { user } = useAuth();
  const [tournamentDetails, setTournamentDetails] = useState(null)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect( () => {
    getTournament(eventId, tournamentId)
      .then((fetchedTournament) => setTournamentDetails(fetchedTournament))
      .catch((err) => setError(err.message || 'Unable to load tournament details'))
      .finally(() => setIsLoading(false))
  }, [eventId, tournamentId])

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!tournamentDetails) return <p>Tournament Details not found</p>
  
  return (
    <>
      <div className="tournament-header-details-container">
        <h2>{tournamentDetails.name}</h2>
        <h3>{tournamentDetails.line_up_type}--{tournamentDetails.game}--{tournamentDetails.platform}</h3>
        <h3>{tournamentDetails.start_time}</h3>
      </div>

      <div className="tournament-registration-container">
        <h2>Register now!</h2>
        <h3>Deadline: {tournamentDetails.registration_deadline}</h3>
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

      <div>
        <Link to={`/events/${eventId}/tournaments/${tournamentId}/standings`}><h2>Standings</h2></Link>
      </div>

      <div>
        <Link to={`/events/${eventId}/tournaments/${tournamentId}/bracket`}><h2>Bracket</h2></Link>
      </div>
    </>
  )
}

export default TournamentDetails;