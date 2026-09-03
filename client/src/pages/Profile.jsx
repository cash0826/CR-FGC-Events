import { useAuth } from "../hooks/useAuth";

function Profile() {
  const { user, logout, isLoading } = useAuth();

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <h2>Your Profile</h2>
      {user.profile_pic_url ? <img src={user.profile_pic_url} alt={user.username}></img> : <p>No image</p> }
      <p>{user.username}</p>
      <p>{user.full_name}</p>
      <p>{user.email}</p>
      <>{user.contact_number}</>
      <button type="button" onClick={logout}>Log out</button>
    </div>
  )
}

export default Profile;