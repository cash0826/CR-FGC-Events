import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { createEventTournament } from "../services/tournamentService";
import DateTimePicker from "../components/DateTimePicker";
import BackButton from "../components/BackButton";

function AddTournament() {
  const { eventId } = useParams();
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();
  // Controlled input using form
  const [form, setForm] = useState({
    name: '',
    start_time: new Date(),
    registration_deadline: new Date(),
    game: '',
    platform: '',
    line_up_type: '',
    event_id: parseInt(eventId),
  })

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      const newTournament = await createEventTournament(eventId, form)
      navigate(`/events/${eventId}/tournaments/${newTournament.id}`)
    } catch (err) {
      setError(err.message || 'Unable to create a new tournament for event')
    } finally {
      setIsSubmitting(false)
    }
  }

  function handleChange(e) {setForm({...form, [e.target.name]: e.target.value})}

  return (
    <>
      <BackButton/>
      <h2>Add a new tournament to an existing event:</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Name of the tournament:
          <input
            name="name"
            value={form.name}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Start Time:
          <DateTimePicker
            name="start_time"
            value={form.start_time}
            onChange={(dt)=> setForm({...form, start_time: dt})}
            required
          />
        </label>
        <label>
          Registration Deadline:
          <DateTimePicker
            name="registration_deadline"
            value={form.registration_deadline}
            onChange={(dt)=> setForm({...form, registration_deadline: dt})}
            required
          />
        </label>
        <label>
          Game:
          <input
            name="game"
            value={form.game}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Platform:
          <input
            name="platform"
            value={form.platform}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Line Up Type:
          <input
            name="line_up_type"
            placeholder="1v1, Teams..."
            value={form.line_up_type}
            onChange={handleChange}
            required
          />
        </label>
        {error && <p role="alert">{error}</p>}
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Adding...' : 'Add a new tournament'}
        </button>
      </form>
    </>
  )
}

export default AddTournament;