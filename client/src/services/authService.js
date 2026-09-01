import { api } from "./api";

// Basic Authorization
export function signup(userData) {
  return api.post('/signup', userData)
}

export function login(userData) {
  return api.post('/login', userData)
}

export function getCurrentUser() {
  return api.get('/me')
}

// Profile - GET/PATCH
export function getProfile() {
  return api.get('/profile')
}

export function updateProfile(userId, updatedProfile) {
  return api.patch(`/profile/${userId}`, updatedProfile)
}