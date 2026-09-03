import { useAuth } from "../hooks/useAuth";

function Profile() {
  const { user, logout, isLoading } = useAuth();

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <h2>Your Profile</h2>
      {user.profile_pic_url ? <img src={user.profile_pic_url} alt={user.username}></img> : <p>No image</p> }
      <h3>Username:</h3><p>{user.username}</p>
      <h3>Name:</h3><p>{user.full_name}</p>
      <h3>Email:</h3><p>{user.email}</p>
      <h3>Phone to Contact:</h3><p>{user.contact_number}</p>
      <button type="button" onClick={logout}>Log out</button>
    </div>
  )
}

export default Profile;