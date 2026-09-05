

function CompetitorRow({ competitor }) {
  console.log(competitor.id)

  return (
    <>
      <p>{competitor.user.username}</p>
    </>
  )
}

export default CompetitorRow;