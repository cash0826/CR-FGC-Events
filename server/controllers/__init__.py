from .auth_controller import Me, Register, Login
from .user_controller import Users, Profile
from .user_role_controller import UserRoles
from .event_controller import Events, ViewEventDetails
from .tournament_controller import EventTournaments, ViewTournamentDetails
from .tournament_competitor_controller import Competitors
from .match_controller import ViewMatches, Matches

__all__ = [
  'Me',
  'Register',
  'Login',
  'Users',
  'Profile',
  'UserRoles',
  'Events', 
  'ViewEventDetails',
  'EventTournaments',
  'ViewTournamentDetails',
  'Competitors',
  'ViewMatches',
  'Matches'
]