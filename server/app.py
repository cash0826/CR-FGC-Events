from config import app, db, bcrypt, jwt, api
from models import (
    User, Role, UserRole, 
    Event, EventAttendee, 
    Tournament, TournamentCompetitor, 
    Match, Player, Standing, Bracket
)
from controllers import (
    Me, Register, Login,
    Users, Profile,
    UserRoles,
    Events, ViewEventDetails,
    EventTournaments, ViewTournamentDetails,
)

# Resources / Controllers

# --- Auth ---
api.add_resource(Me, '/api/me')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')

# --- User ---
api.add_resource(Users, '/api/users', '/api/users/<int:id>')
api.add_resource(Profile, '/api/profile', '/api/profile/<int:id>')

# --- UserRoles ---
api.add_resource(
    UserRoles, 
    '/api/users/<int:user_id>/roles',
    '/api/users/<int:user_id>/roles/<string:role_name>'
)

# --- Events ---
api.add_resource(Events, '/api/events', '/api/events/<int:id>')
api.add_resource(ViewEventDetails, '/api/events/<int:id>')

# --- Tournaments ---
api.add_resource(
    EventTournaments, 
    '/api/events/<int:event_id>/tournaments',
    '/api/events/<int:event_id>/tournaments/<int:tournaments_id>'
)
api.add_resource(
    ViewTournamentDetails,
    '/api/events/<int:event_id>/tournaments/<int:tournaments_id>'
)

if __name__ == "__main__":
    app.run(debug=True, port=5555)