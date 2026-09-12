import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { createEventTournament } from "../services/tournamentService";
import DateTimePicker from "../components/DateTimePicker";
import BackButton from "../components/BackButton";
import NavBar from '../components/NavBar'

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
      <header>
        <NavBar/>
      </header>

      <main>
        <section >
          <div className="form-container">
            <div className="row-header">
              <h1>Add a tournament:</h1>
            </div>
            <div className="row-form">
              <form onSubmit={handleSubmit}>
                <input
                  placeholder="Name"
                  value={form.name}
                  onChange={handleChange}
                  required
                />
                <DateTimePicker
                  placeholder="Start Time"
                  value={form.start_time}
                  onChange={(dt)=> setForm({...form, start_time: dt})}
                  required
                />
                <DateTimePicker
                  placeholder="Registration Deadline"
                  value={form.registration_deadline}
                  onChange={(dt)=> setForm({...form, registration_deadline: dt})}
                  required
                />
                <input
                  placeholder="Game"
                  value={form.game}
                  onChange={handleChange}
                  required
                />
                <input
                  placeholder="Platform"
                  value={form.platform}
                  onChange={handleChange}
                  required
                />
                <input
                  placeholder="1v1 (Singles), Teams..."
                  value={form.line_up_type}
                  onChange={handleChange}
                  required
                />
                {error && <p role="alert">{error}</p>}
                <button type="submit" disabled={isSubmitting}>
                  {isSubmitting ? 'Adding...' : 'Add a new tournament'}
                </button>
              </form>
            </div>
          </div>
        </section>
        <BackButton/>
      </main>
    </>
  )
}

export default AddTournament;