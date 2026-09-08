from random import choice as rc
from faker import Faker
import datetime as dt
from config import app, db
from models import (
    User, Role, UserRole, 
    Event, Tournament, TournamentCompetitor
)

fake = Faker()

with app.app_context():
  # Delete all rows and columns in current tables
  print('Deleting all records...')
  User.query.delete()
  UserRole.query.delete()
  Role.query.delete()
  Event.query.delete()
  Tournament.query.delete()
  TournamentCompetitor.query.delete()
  
  # Creates roles: admin, host, player, viewer
  print("Creating admin, host, player and viewer roles...")
  role_admin = Role(
    name = "admin",
    description = "Administrator of site users, tournaments and events.",
    is_system_role = True
  )
  role_host = Role(
    name = "host",
    description = "Create and manage tournaments.",
    is_system_role = False
  )
  role_player = Role(
    name = "player",
    description = "Play in tournament matches. Visible profile username.",
    is_system_role = False
  )
  role_viewer = Role(
    name = "viewer",
    description = "read-only",
    is_system_role = False
  )
  db.session.add_all([role_admin, role_host, role_player, role_viewer])
  
  # Creates admin and 2 host accounts
  print("Creating a test admin account and two host accounts...")
  admin = User(
    email='admin@email.com',
    username='admin_user',
    full_name='Melanie Rodriguez'
  )
  admin.password_hash = 'adminpassword'

  host1 = User(
    email= 'host1@email.com',
    username= 'host1_user',
    full_name= 'Host1'
  )
  host1.password_hash = 'host1password'

  host2 = User(
    email= 'host2@email.com',
    username= 'host2_user',
    full_name= 'Host2'
  )
  host2.password_hash = 'host2password'
  
  db.session.add_all([admin, host1, host2])
  db.session.commit()
  
  # Creates 30 players
  print("Creating 30 test players...")
  players = []
  for i in range(30):
    name = fake.unique.first_name()
    email = name.lower() + '@email.com'
    random_int = fake.random_int(min=1, max=399)
    username = f"{name.lower()}{random_int}"
    password = name.lower() + 'password'
    player = User(
      email=email,
      username=username,
      full_name=name
    )
    player.password_hash = password
    players.append(player)
  db.session.add_all(players)
  db.session.commit()
  
  # Assigns admin, host and player roles
  print("Assigning admin, host and player roles... ")
  
  admin_role_lookup = Role.query.filter_by(name="admin").first()    # Assign admin role
  admin_role = UserRole(user_id=admin.id, role_id=admin_role_lookup.id)
  
  host_role_lookup = Role.query.filter_by(name="host").first()    # Assign host role
  host1_role = UserRole(user_id=host1.id, role_id=host_role_lookup.id)
  host2_role = UserRole(user_id=host2.id, role_id=host_role_lookup.id)  

  player_roles = []
  player_role_lookup = Role.query.filter_by(name="player").first()    # Assign player role  
  for player in players:
    player_role = UserRole(user_id=player.id, role_id=player_role_lookup.id)
    player_roles.append(player_role)
  
  db.session.add_all([admin_role, host1_role, host2_role, player_role])
  db.session.add_all(player_roles)
  db.session.commit()
  
  # Creating 5 events
  print("Creating 10 test events...")
  events = []
  for i in range(10):
    name = f"Event{i+1}"
    start = fake.date_between_dates(date_start=dt.date(2026, 9, 19), date_end=dt.date(2026, 10, 3))
    end = start + dt.timedelta(days=1)
    in_person = rc([True, False])
    location = rc(["San Pedro", "Barreal, Heredia", "Coronado"])
    description = "Lorem ipsum dolor sit amet consectetur adipiscing elit."
    tie_breaking_rule = "Consectetur adipiscing elit quisque faucibus ex sapien vitae."
    host = rc([host1, host2])
    event = Event(
      name=name,
      start=start,
      end=end,
      in_person=in_person,
      location=location,
      description=description,
      tie_breaking_rule=tie_breaking_rule,
      host=host
    )
    events.append(event)
  db.session.add_all(events)
  db.session.commit()
    
  # Creating 20 tournaments
  print("Creating 20 test tournaments...")
  tournaments = []
  for i in range(20):
    name = rc(["SF", "MK", "FF"])
    start_time = fake.date_time_between(start_date=dt.date(2026, 9, 19), end_date=dt.date(2026, 10, 3))
    registration_deadline = fake.date_between(start_date='-1w')
    platform = rc(["PS4", "PS5", "XBOX"])
    line_up_type = "Singles"
    tournament = Tournament(
      name=name,
      start_time=start_time,
      registration_deadline=registration_deadline,
      game=name,
      platform=platform,
      line_up_type=line_up_type,
    )
    tournament.event = rc(events)
    tournaments.append(tournament)
  db.session.add_all(tournaments)
  db.session.commit()
  
  # Register players to tournaments
  print("Registering random number of players to each tournament...")
  competitors = []
  for tournament in tournaments:
    ran_total = fake.random_int(min=10, max=40)
    for i in range(ran_total):
      ran_player = rc(players)
      competitor = TournamentCompetitor(user_id=ran_player.id, tournament_id=tournament.id)
      competitors.append(competitor)
  db.session.add_all(competitors)
  db.session.commit()
  
  print("Database seeded successfully! 🌱")
  print("Use 'adminpassword', 'host1password', 'host2password'.")
  print("Use player's name in lower case + 'password' for the password")
  
  

  