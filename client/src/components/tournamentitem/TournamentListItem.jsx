import { Link } from 'react-router-dom'

function TournamentListItem({ event, tournament }) {
  return (
    <>
      <Link to={`/events/${event.id}/tournaments/${tournament.id}`}>{tournament.name}({tournament.platform})</Link>
    </>
  )
}

export default TournamentListItem;