import { Link } from 'react-router-dom'
import { formatLongDate } from "../../utils/dateUtils"

function EventListItem({ event }) {
  return (
    <li>
      <Link to={`/events/${event.id}`}><strong>{event.name}</strong></Link>
      <p>Start: {formatLongDate(event.start)}</p>
      <p>Location: {event.location}</p>
      <p>Host: {event.host.username}</p>
    </li>
  )
}

export default EventListItem;