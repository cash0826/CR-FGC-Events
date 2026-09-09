import { useState } from "react";
import { useParams, useOutletContext } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import StandingRow from "../components/standings/StandingRow";

function Standings() {
  const { eventId, tournamentId } = useParams();
  const { user } = useAuth();
  const { event } = useOutletContext()
  const [standings, setStandings] = useState(null);
  const [error, setError] = useState('');

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