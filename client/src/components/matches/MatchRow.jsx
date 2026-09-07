

function MatchRow({ match }) {

  return (
    <>
      <p>{match.round}-{match.status}</p>
      <p>{match.start_time}</p>
    </>
  )
}

export default MatchRow;