import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { listStandings } from "../services/standingService";
import StandingRow from "../components/standings/StandingRow";

function Standings() {
  const { eventId, tournamentId } = useParams();
  const { user } = useAuth();
  const [standings, setStandings] = useState(null)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    listStandings(eventId, tournamentId)
      .then((fetchedStandings) => setStandings(fetchedStandings))
      .catch((err) => setError(err.message || 'Unable to load standings'))
      .finally(() => setIsLoading(false))
  }, [eventId, tournamentId])

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!standings) return <p>Standings not found</p>
  if (standings.length === 0) return <p> No Standings posted yet</p>

  return (
    <>
      <div className="standings-standing-container">
        {standings.map((standing)=> (
          <StandingRow
            key={standing.id}
            standing={standing}
          />
        ))}
      </div>
    </>
  )
}

export default Standings;