import { useState, useEffect } from "react";
import { useParams, useOutletContext } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { getBracket } from "../services/bracketService";

function Bracket() {
  const { eventId, tournamentId } = useParams();
  const { user } = useAuth();
  const { event } = useOutletContext()
  const [bracket, setBracket] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    getBracket(eventId, tournamentId)
      .then((fetchedBracket) => setBracket(fetchedBracket))
      .catch((err) => setError(err.message || 'Unable to load bracket'))
      .finally(() => setIsLoading(false))
  }, [eventId, tournamentId])

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!bracket) return <p>Bracket not found</p>
  if (Object.keys(bracket).length === 0) return <p>No Bracket posted yet</p>

  return (
    <>
      <div className="bracket-container">
        <p>{bracket.url}</p>
      </div>
    </>
  )
}

export default Bracket;