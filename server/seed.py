from random import choice
from faker import Faker
import datetime
from config import app, db
from models import (
    User, Role, UserRole, 
    Event, EventAttendee, 
    Tournament, TournamentCompetitor, 
    Match, Player, Standing, Bracket
)

fake = Faker()

with app.app_context():
  # Delete all rows and columns in current tables
  print('Deleting all records')
  User.query.delete()
  UserRole.query.delete()
  Role.query.delete()
  Event.query.delete()
  EventAttendee.query.delete()
  Tournament.query.delete()
  TournamentCompetitor.query.delete()
  Bracket.query.delete()
  Standing.query.delete()
  Match.query.delete()
  Player.query.delete()
  
  # Creates 2 Users
  print("Creating admin and test acct. Use 'admminpassword' and 'testpassword'")
  admin = User(
    email='admin@email.com',
    username='admin_user',
    full_name='Melanie Rodriguez',
    date_of_birth=datetime.date(1996, 8, 26),
  )
  admin.password_hash = 'adminpassword'
  
  test = User(
    email= 'test@email.com',
    username= 'test_user',
    full_name= 'John Doe',
    date_of_birth=datetime.date(1990, 1, 1),
  )
  test.password_hash = 'testpassword'
  
  db.session.add(admin)
  db.session.add(test)
  # ALT: db.session.add_all([admin, test])
  db.session.commit()
  
  # 