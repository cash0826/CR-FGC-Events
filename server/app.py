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
    Events, ViewEventDetails
)

# Resources / Controllers

# --- AuthController ---
api.add_resource(Me, '/api/me')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')

# --- UserController ---
api.add_resource(Users, '/api/users', '/api/users/<int:id>')
api.add_resource(Profile, '/api/profile', '/api/profile/<int:id>')

# --- EventsController ---
api.add_resource(Events, '/api/events', '/api/events/<int:id>')
api.add_resource(ViewEventDetails, '/api/events/<int:id>')

# --- TournamentsController ---

if __name__ == "__main__":
    app.run(debug=True, port=5555)