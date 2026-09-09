import { useState } from "react";
import { useParams, useOutletContext } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { createMatch } from "../services/matchService";
import MatchRow from "../components/matches/MatchRow";
import DateTimePicker from "../components/DateTimePicker";

function Matches() {
  const { eventId, tournamentId } = useParams();
  const { event } = useOutletContext()
  const { user } = useAuth();
  const tournament = event.tournaments.find((t) => String(t.id) === String(tournamentId)) || null
  const [matches, setMatches] = useState(tournament.matches)
  const [isOpen, setIsOpen] = useState(false)
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [form, setForm] = useState({
    round: '',
    start_time: new Date(),
    status: '',
    tournament_id: tournamentId,
  })

  const isOwner = Boolean(tournament && user && event.host_id === user.id)
  const isAdmin = Boolean(tournament && user?.roles?.some(userRole => userRole.role?.name === "admin"))

  async function handleAdd(e) {
    setIsSubmitting(true)
    try {
      const newMatch = await createMatch(eventId, tournamentId, form)
      setMatches((current) => [newMatch, ...current])
    } catch (err) {
      setError(err.message || 'Unable to add a match')
    } finally {
      setIsSubmitting(false)
      setIsOpen(false)
    }
  }

  const isEmpty = Boolean(matches.length === 0)
  if (!matches) return <p>Matches not found</p>

  return (
    <>
      <div className="matches-match-container">
        {isEmpty ? (
          <>
            <p>No matches posted yet.</p>
          </>
        ) : (
          <>
            {matches.map((match) => (
                <MatchRow
                  key={match.id}
                  match={match}
                  eventId={eventId}
                  tournamentId={tournamentId}
                  isOwner={isOwner}
                  isAdmin={isAdmin}
                  setMatches={setMatches}
                />
            ))}
          </>
        )}
        <div className="matches-add-match">
          {isOpen ? (
            <>
              <label>Round:</label>
              <input
                name="round"
                value={form.round}
                onChange={(e)=> setForm({...form, round: e.target.value})}
                required
              />
              <label>Start_time:</label>
              <DateTimePicker
                name="start_time"
                value={form.start_time}
                onChange={(dt)=> setForm({...form, start_time: dt})}
                required
              />
              <label>Status:</label>
              <input
                name="status"
                placeholder="pending, in_progress, cancelled, completed"
                value={form.status}
                onChange={(e)=> setForm({...form, status: e.target.value})}
              />
              <button onClick={handleAdd} disabled={isSubmitting}>
                {isSubmitting ? 'Adding...' : 'Confirm New Match'}
              </button>
              <button onClick={()=> setIsOpen(false)}>Cancel</button>
              {error && <p role="alert">{error}</p>}
            </>
          ) : (
            <>
              {(isOwner || isAdmin) && (
                <button onClick={()=> setIsOpen(true)}>Add a Match</button>
              )}
            </>
          )}
        </div>
      </div>
    </>
  )
}

export default Matches;
