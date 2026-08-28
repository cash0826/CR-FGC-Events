import json
import pytest
from app import app, db
from models.roles import Role
from models.user_roles import UserRole


@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        # Ensure standard roles exist
        for r in ["admin", "host", "player", "viewer"]:
            if not Role.query.filter_by(name=r).first():
                db.session.add(Role(name=r, description=f"{r} role", is_system_role=True))
        db.session.commit()

        with app.test_client() as client:
            yield client

        db.session.remove()
        db.drop_all()


def register_user(client, email, username, password, full_name="Test User", dob="1990-01-01"):
    payload = {
        "email": email,
        "username": username,
        "password": password,
        "full_name": full_name,
        "date_of_birth": dob
    }
    resp = client.post('/api/register', json=payload)
    return resp


def login_user(client, email, password):
    resp = client.post('/api/login', json={"email": email, "password": password})
    return resp


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}
    return {"Authorization": f"Bearer {token}"}


def auth_bearer(token):
    return {"Authorization": f"Bearer {token}"}


def test_register_login_and_me(client):
    # Register
    r = register_user(client, 'alice@example.com', 'alice', 'password123')
    assert r.status_code == 201
    data = r.get_json()
    assert 'token' in data
    token = data['token']
    user = data['user']
    assert user['email'] == 'alice@example.com'

    # Use token for /api/me
    me = client.get('/api/me', headers=auth_bearer(token))
    assert me.status_code == 200
    me_data = me.get_json()
    assert me_data['email'] == 'alice@example.com'


def test_event_tournament_and_match_flow(client):
    # Register a user and give them host role so they can create events
    r = register_user(client, 'host@example.com', 'hostuser', 'password123')
    assert r.status_code == 201
    token = r.get_json()['token']
    user = r.get_json()['user']
    user_id = user['id']

    # Assign host role directly in DB
    host_role = Role.query.filter_by(name='host').first()
    assert host_role is not None
    if not UserRole.query.filter_by(user_id=user_id, role_id=host_role.id).first():
        db.session.add(UserRole(user_id=user_id, role_id=host_role.id))
        db.session.commit()

    # Create event, tournament and match directly via services (avoid POST serialization issues)
    from services.events_service import EventService
    from services.tournaments_service import TournamentService
    from services.matches_service import MatchService

    from datetime import datetime
    new_event, err = EventService.create({
        "name": "Test Event",
        "start": datetime.fromisoformat("2026-09-01T10:00:00"),
        "host_id": user_id
    })
    assert err is None
    event_id = new_event.id

    from datetime import datetime
    new_tourn, err = TournamentService.create_tournament(event_id=event_id, data={
        "name": "Test Tournament",
        "start_time": datetime.fromisoformat("2026-09-02T10:00:00"),
        "registration_deadline": datetime.fromisoformat("2026-09-01T12:00:00"),
        "line_up_type": "singles"
    })
    assert err is None
    tournament_id = new_tourn.id

    new_match, err = MatchService.create({"tournament_id": tournament_id, "round": "1"})
    assert err is None
    match_id = new_match.id

    # Fetch events list (public)
    evl = client.get('/api/events')
    assert evl.status_code == 200
    evdata = evl.get_json()
    assert isinstance(evdata['events'], list)

    # Fetch event detail
    ved = client.get(f'/api/events/{event_id}')
    assert ved.status_code == 200

    # Fetch matches list and detail (public GETs)
    ml = client.get(f'/api/events/{event_id}/tournaments/{tournament_id}/matches')
    assert ml.status_code == 200
    matches = ml.get_json()
    assert isinstance(matches, list)

    md = client.get(f'/api/events/{event_id}/tournaments/{tournament_id}/matches/{match_id}')
    assert md.status_code == 200
    match_detail = md.get_json()
    assert match_detail['id'] == match_id


def test_admin_and_controller_post_delete_flows(client):
    # Create an admin user and assign admin role
    r = register_user(client, 'admin@example.com', 'adminuser', 'password123')
    assert r.status_code == 201
    admin_token = r.get_json()['token']
    admin_user = r.get_json()['user']
    admin_id = admin_user['id']

    admin_role = Role.query.filter_by(name='admin').first()
    assert admin_role is not None
    if not UserRole.query.filter_by(user_id=admin_id, role_id=admin_role.id).first():
        db.session.add(UserRole(user_id=admin_id, role_id=admin_role.id))
        db.session.commit()

    # Admin: list users
    ul = client.get('/api/users', headers=auth_bearer(admin_token))
    assert ul.status_code == 200
    users_payload = ul.get_json()
    assert 'users' in users_payload

    # Admin: create a new user via admin endpoint
    new_payload = {
        'email': 'newuser@example.com',
        'username': 'newuser',
        'password': 'pass1234',
        'full_name': 'New User',
        'date_of_birth': '1992-02-02'
    }
    cr = client.post('/api/users', json=new_payload, headers=auth_bearer(admin_token))
    assert cr.status_code == 201
    created = cr.get_json()
    created_id = created['id']

    # Admin: patch user
    patch = client.patch(f'/api/users/{created_id}', json={'full_name': 'Updated Name'}, headers=auth_bearer(admin_token))
    assert patch.status_code == 200
    assert patch.get_json()['full_name'] == 'Updated Name'

    # Admin: delete user
    dl = client.delete(f'/api/users/{created_id}', headers=auth_bearer(admin_token))
    assert dl.status_code == 200

    # --- Competitors / Standings / Bracket flows (controller-level) ---
    # Create host and competitor users
    rh = register_user(client, 'host2@example.com', 'host2', 'password123')
    assert rh.status_code == 201
    host_token = rh.get_json()['token']
    host_user = rh.get_json()['user']
    host_id = host_user['id']
    host_role = Role.query.filter_by(name='host').first()
    if not UserRole.query.filter_by(user_id=host_id, role_id=host_role.id).first():
        db.session.add(UserRole(user_id=host_id, role_id=host_role.id))
        db.session.commit()

    rc = register_user(client, 'comp@example.com', 'compy', 'password123')
    assert rc.status_code == 201
    comp_token = rc.get_json()['token']
    comp_user = rc.get_json()['user']
    comp_id = comp_user['id']

    # Create event and tournament via services (host is owner)
    from services.events_service import EventService
    from services.tournaments_service import TournamentService
    from datetime import datetime

    new_event, err = EventService.create({
        'name': 'Controller Event',
        'start': datetime.fromisoformat('2026-10-01T10:00:00'),
        'host_id': host_id
    })
    assert err is None
    event_id = new_event.id

    new_tourn, err = TournamentService.create_tournament(event_id=event_id, data={
        'name': 'Controller Tourney',
        'start_time': datetime.fromisoformat('2026-10-02T10:00:00'),
        'registration_deadline': datetime.fromisoformat('2026-10-01T12:00:00'),
        'line_up_type': 'singles'
    })
    assert err is None
    tournament_id = new_tourn.id

    # Competitor registers via controller POST
    crep = client.post(f'/api/events/{event_id}/tournaments/{tournament_id}/competitors', headers=auth_bearer(comp_token))
    assert crep.status_code == 201
    competitor = crep.get_json()
    comp_rec_id = competitor['id']

    # Host deletes competitor via controller DELETE
    delc = client.delete(f'/api/events/{event_id}/tournaments/{tournament_id}/competitors/{comp_rec_id}', headers=auth_bearer(host_token))
    assert delc.status_code == 200

    # Re-register competitor for standings/bracket
    crep2 = client.post(f'/api/events/{event_id}/tournaments/{tournament_id}/competitors', headers=auth_bearer(comp_token))
    assert crep2.status_code == 201
    competitor2 = crep2.get_json()
    comp_rec_id2 = competitor2['id']

    # Create standing via controller POST (host)
    standing_payload = {'competitor_id': comp_rec_id2, 'points': 5}
    sr = client.post(f'/api/events/{event_id}/tournaments/{tournament_id}/standings', json=standing_payload, headers=auth_bearer(host_token))
    assert sr.status_code == 201
    standing = sr.get_json()
    standing_id = standing['id']

    # Delete standing
    ds = client.delete(f'/api/events/{event_id}/tournaments/{tournament_id}/standings/{standing_id}', headers=auth_bearer(host_token))
    assert ds.status_code == 200

    # Create bracket
    br_payload = {'url': 'http://example.com/bracket'}
    br = client.post(f'/api/events/{event_id}/tournaments/{tournament_id}/bracket', json=br_payload, headers=auth_bearer(host_token))
    assert br.status_code == 201
    bracket = br.get_json()
    bracket_id = bracket['id']

    # Patch bracket
    pbr = client.patch(f'/api/events/{event_id}/tournaments/{tournament_id}/bracket/{bracket_id}', json={'url': 'http://changed.example/bracket'}, headers=auth_bearer(host_token))
    assert pbr.status_code == 200
    assert pbr.get_json()['url'] == 'http://changed.example/bracket'

    # Delete bracket
    dbr = client.delete(f'/api/events/{event_id}/tournaments/{tournament_id}/bracket/{bracket_id}', headers=auth_bearer(host_token))
    assert dbr.status_code == 200
