import { Link } from 'react-router-dom'

function TournamentListItem({ event, tournament }) {
  return (
    <>
      <Link to={`/events/${event.id}/tournament/${tournament.id}`}>{tournament.name}({tournament.platform})</Link>
    </>
  )
}

export default TournamentListItem;