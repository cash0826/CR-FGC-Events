import { Link } from 'react-router-dom'
import { formatLongDate } from "../../utils/dateUtils"

function EventItem({ event }) {
  return (
    <>
      <Link to={`/events/${event.id}`}><h2><strong>{event.name}</strong></h2></Link>
      <p>Start: {formatLongDate(event.start)}</p>
      <p>Location: {event.location}</p>
      <p>Host: {event.host.username}</p>
    </>
  )
}

export default EventItem;