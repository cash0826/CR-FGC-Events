

function EventListItem({ event }) {
  return (
    <li>
      <strong>{event.name}</strong>({event.start})
      <p>{event.description}</p>
      <p>{event.tie_breaking_rule}</p>
      <p>{event.host.username}</p>
    </li>
  )
}

export default EventListItem;