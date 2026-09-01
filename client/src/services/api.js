const BASE_URL = import.meta.env.VITE_API_URL || '/api'

export async function apiFetch(path, { headers, ...options } ={} ) {
  const token = localStorage.getItem("accessToken")

  const response = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {} ),
      ...headers,
    },
    ...options
  })

  // Handle no body responses
  if (response.status === 204) {
    return null
  }

  const data = await response.json().catch( ()=> null)

  // Throw errors
  if (!response.ok) {
    const errorData = await response.json().catch( ()=> ({}));
    const msg = 
      errorData.error || `Request failed with status ${response.status}`
    throw new Error(msg);
    return null
  }

  return data
}

export const api = {
  get: (path) => apiFetch(path),
  post: (path, body) => apiFetch(path, { method: 'POST', body: JSON.stringify(body) }),
  put: (path, body) => apiFetch(path, { method: 'PUT', body: JSON.stringify(body) }),
  delete: (path) => apiFetch(path, { method: 'DELETE' }),
}