import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { getTournament } from "../services/tournamentService";
import CompetitorRow from "../components/competitors/CompetitorRow";

// Public (Read and register to tournament)
// If event owner or admin, POST/PATCH/DEL

function TournamentDetails() {
  const { eventId, tournamentId } = useParams();
  const { user } = useAuth();
  const [tournamentDetails, setTournamentDetails] = useState(null)
  const [competitors, setCompetitors] = useState([])
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect( () => {
    Promise.all([getTournament(eventId, tournamentId) ])
    .then(([fetchedTournament, fetchedCompetitors]) => {
      setTournamentDetails(fetchedTournament)
      setCompetitors(fetchedCompetitors)
    })
    .catch((err) => setError(err.message || 'unable to load tournament details'))
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
        <h2>Registered Competitors:</h2>
        <ul>
          <li>
            {tournamentDetails.competitors.map((competitor) => {
              <CompetitorRow
                key={competitor.id}
                competitor={competitor}
              />
            })}
          </li>
        </ul>
      </div>
    </>
  )
}

export default TournamentDetails;