from .auth_controller import Me, Register, Login
from .user_controller import Users, Profile
from .event_controller import Events, ViewEventDetails
from .tournament_controller import EventTournaments, ViewTournamentDetails

__all__ = [
  'Me',
  'Register',
  'Login',
  'Users',
  'Profile',
  'Events', 
  'ViewEventDetails',
  'EventTournaments',
  'ViewTournamentDetails'
]