import { useAuth } from "../hooks/useAuth";
import { useState } from "react";
import { updateProfile } from "../services/authService";

function Profile() {
  const { user, setUser, logout, isLoading } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    email: '',
    username: '',
    full_name: '',
    bio: '',
    profile_pic_url: '',
    contact_number: ''
  })

  // Toggle inline editing
  function startEditing() {
    setError('')
    setForm({
      email: user.email,
      username: user.username,
      full_name: user.full_name,
      bio: user.bio,
      profile_pic_url: user.profile_pic_url,
      contact_number: user.contact_number
    })
    setIsEditing(true)
  }

  // Update
  async function handleSave(e) {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      const updated = await updateProfile(user.id, form)
      setUser(updated)
      setIsEditing(false)
    } catch (err) {
      setError(err.message || 'Unable to update profile')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isLoading) return <p>Loading...</p>;

  return (
    <div className="profile">
      {isEditing ? (
        <form>
          <label>Profile Picture</label>
          <input
            type="url"
            value={form.profile_pic_url}
            onChange={(e) => setForm({...form, profile_pic_url: e.target.value})}
          />
          <label>Username</label>
          <input
            value={form.username}
            onChange={(e) => setForm({...form, username: e.target.value})}
          />
          <label>Name</label>
          <input
            value={form.full_name}
            onChange={(e) => setForm({...form, full_name: e.target.value})}
          />
          <label>Email</label>
          <input
            type="email"
            value={form.email}
            onChange={(e) => setForm({...form, email: e.target.value})}
          />
          <label>Phone to Contact</label>
          <input
            type="tel"
            value={form.contact_number}
            onChange={(e) => setForm({...form, contact_number: e.target.value})}
          />
          <label>Biography</label>
          <textarea
            value={form.bio}
            onChange={(e) => setForm({...form, bio: e.target.value})}
          />
          <button onClick={handleSave} disabled={isSubmitting}>
            {isSubmitting ? 'Saving...' : 'Save'}
          </button>
          <button onClick={() => setIsEditing(false)}>Cancel</button>
          {error && <p role="alert">{error}</p>}
        </form>
      ) : (
        <>
          <h2>Your Profile</h2>
          {user.profile_pic_url ? <img src={user.profile_pic_url} alt={user.username}></img> : <p>No image</p> }
          <h3>Username:</h3><p>{user.username}</p>
          <h3>Name:</h3><p>{user.full_name}</p>
          <h3>Email:</h3><p>{user.email}</p>
          {user.contact_number && (
            <>
              <h3>Phone to Contact:</h3>
              <p>{user.contact_number}</p>
            </>
          )}
          {user.bio && (
            <>
              <h3>Biography:</h3>
              <p>{user.bio}</p>
            </>
          )}
          <button onClick={startEditing}>Edit Profile Details</button>
          <button type="button" onClick={logout}>Log out</button>
        </>
      )}
    </div>
  )
}

export default Profile;