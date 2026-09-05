import { useState, useEffect } from "react";
import { listEvents } from "../services/eventService";
import EventListItem from "../components/eventitem/EventListItem";

function Home() {
  const [events, setEvents] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect( ()=> {
    listEvents()
      .then((data) => {
        setEvents( data.events || [] );
        setIsLoading(false)
      })
      .catch((error)=> {
        console.error("Error retrieving events: ", error )
        setError("Unable to load Events")
      })
  }, []);

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (events.message) return <p>{events.message}</p>;

  return (
    <>
      <header>
        <h1>CR FGC Upcoming Events</h1>
      </header>
      <main>
        <ul>
          {events.map((event) => (
            <EventListItem 
              key={event.id}
              event={event}
            />
          ))}
        </ul>
      </main>
    </>
  )
}

export default Home;