import { useState } from "react";
import { createEvent } from "../services/eventService";
import DateTimePicker from "../components/DateTimePicker"

function CreateEvent() {

  // Controlled input for form
  const [form, setForm] = useState({
    name: '',
    start: new Date(),
    end: new Date(),
    in_person: false,
    location: '',
    description: '',
  })

  async function handleSubmit(e) {
    return
  }

  return (
    <>
      <h1>Create a new Event to host tournaments:</h1>
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
      </form>
    </>
  )
}

export default CreateEvent;
