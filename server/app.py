from config import app, db, bcrypt, jwt, api
from models import (
    User, Role, UserRole, 
    Event, EventAttendee, 
    Tournament, TournamentCompetitor, 
    Match, Player, Standing, Bracket
)

if __name__ == "__main__":
    app.run(debug=True, port=5555)
