import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { createEvent } from "../services/eventService";
import DateTimePicker from "../components/DateTimePicker"
import BackButton from "../components/BackButton";

function CreateEvent() {
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { user } = useAuth();
  const navigate = useNavigate();
  // Controlled input for form
  const [form, setForm] = useState({
    name: '',
    start: new Date(),
    end: new Date(),
    in_person: false,
    location: '',
    description: '',
    tie_breaking_rule: '',
    host_id: user.id
  })

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      const newEvent = await createEvent(form)
      navigate(`/events/${newEvent.id}`)
    } catch (err) {
      setError(err.message || 'Unable to create event')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <>
      <BackButton/>
      <h2>Create a new Event to host tournaments:</h2>
      <form onSubmit={handleSubmit}> 
        <label>
        Name of the event:
          <input
            value={form.name}
            onChange={(e)=> setForm({...form, name: e.target.value})}
            required
          />
        </label>
        <label>
        Start:
          <DateTimePicker
            value={form.start}
            onChange={(dt)=> setForm({...form, start: dt})}
          />
        </label>
        <label>
        End:
          <DateTimePicker
            value={form.end}
            onChange={(dt)=> setForm({...form, end: dt})}
          />
        </label>
        <label>
        In Person?:
          <input
            type="checkbox"
            checked={form.in_person}
            onChange={(e)=> setForm({...form, in_person: e.target.checked})}
          />
        </label>
        <label>
        Location if in person:
          <input
            placeholder="San Pedro"
            value={form.location}
            onChange={(e)=> setForm({...form, location: e.target.value})}
          />
        </label>
        <label>
        Description:
          <textarea
            placeholder="(Optional) Include all relevant details about the event..."
            value={form.description}
            onChange={(e)=> setForm({...form, description: e.target.value})}
          />
        </label>
        <label>
        Rules:
          <textarea
            placeholder="(Optional) Include any tie breaking rules or general code of conduct..."
            value={form.description}
            onChange={(e)=> setForm({...form, description: e.target.value})}
          />
        </label>
        {error && <p role="alert">{error}</p>}
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Creating Event...' : 'Create New Event'}
        </button>
      </form>
    </>
  )
}

export default CreateEvent;
