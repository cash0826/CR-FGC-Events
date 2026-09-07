

function StandingRow({ standing }) {
  
  return (
    <>
      <p>{standing.competitor_id}--{standing.points}</p>
    </>
  )
}

export default StandingRow;