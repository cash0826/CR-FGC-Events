import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { listMatches } from "../services/matchService";
import MatchRow from "../components/matches/MatchRow";

function Matches() {
  const { eventId, tournamentId } = useParams();
  const { user } = useAuth();
  const [matches, setMatches] = useState(null)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(()=> {
    listMatches(eventId, tournamentId)
      .then((fetchedMatches) => setMatches(fetchedMatches))
      .catch((err) => setError(err.message || 'Unable to load matches'))
      .finally(() => setIsLoading(false))
  }, [eventId, tournamentId])

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!matches) return <p>Matches not found</p>
  if (matches.length === 0) return <p>No Matches posted yet</p>

  return (
    <>
      <div className="matches-match-container">
        {matches.map((match) => (
          <MatchRow
            key={match.id}
            match={match}
          />
        ))}
      </div>
    </>
  )
}

export default Matches;
