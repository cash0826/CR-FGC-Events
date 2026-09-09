import { useState } from "react";
import { useParams, useOutletContext } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";


function Bracket() {
  const { eventId, tournamentId } = useParams();
  const { user } = useAuth();
  const { event } = useOutletContext()
  const [bracket, setBracket] = useState(null);
  const [error, setError] = useState('');

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