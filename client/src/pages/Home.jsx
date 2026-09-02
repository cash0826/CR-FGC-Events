import { useState, useEffect } from "react";
import { Outlet } from "react-router-dom";
import { listEvents } from "../services/eventService";

function Home() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect( ()=> {
    listEvents()
      .then((data) => {
        setEvents( data || [] );
        setLoading(false)
      })
      .catch((error)=> {
        console.error("Error retrieving events: ", error )
        setError("Unable to load Events")
      })
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (events.message) return <p>{events.message}</p>;

  return (
    <>
      <header>
        <h1>CR FGC Upcoming Events</h1>
      </header>
      <main>
        <Outlet context={{ events, setEvents }} />
      </main>
    </>
  )
}

export default Home;