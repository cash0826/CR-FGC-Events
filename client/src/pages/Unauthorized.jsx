import NavBar from '../components/NavBar'

function Unauthorized() {
  return (
    <>
      <header>
        <NavBar/>
        <h1>Unauthorized</h1>
      </header>
      <p>You do not have permission to view this page.</p>
    </>
  );
}

export default Unauthorized;

