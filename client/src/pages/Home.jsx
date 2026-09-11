import { useState, useEffect } from "react";
import { listEvents } from "../services/eventService";
import EventItem from "../components/eventitem/EventItem";
import NavBar from '../components/NavBar'

function Home() {
  const [events, setEvents] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect( ()=> {
    listEvents()
      .then((data) => setEvents( data.events || [] ))
      .catch((err) => setError(err.message || 'Unable to load events'))
      .finally(() => setIsLoading(false))
  }, []);

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (events.message) return <p>{events.message}</p>;

  return (
    <>
      <header>
        <NavBar/>
      </header>
      <main>
        <section className="banner"></section>
        <section>
          {events.map((event) => (
            <EventItem 
              key={event.id}
              event={event}
            />
          ))}
        </section>
      </main>
    </>
  )
}

export default Home;