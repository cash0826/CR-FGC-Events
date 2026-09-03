import pytest
from app import app, db
from models import (
    Bracket,
    Event,
    EventAttendee,
    Match,
    Player,
    Role,
    Standing,
    Tournament,
    TournamentCompetitor,
    User,
    UserRole,
)


@pytest.fixture
def setup_db():
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


def assert_column_set(model, expected_columns):
    table_columns = set(model.__table__.columns.keys())
    missing = set(expected_columns) - table_columns
    assert not missing, f"{model.__name__} missing columns: {sorted(missing)}"


def assert_foreign_key(model, column_name, target_name):
    column = model.__table__.columns[column_name]
    targets = {fk.target_fullname for fk in column.foreign_keys}
    assert target_name in targets, (
        f"{model.__name__}.{column_name} should reference {target_name}, "
        f"got {sorted(targets)}"
    )


def test_role_model_has_expected_columns():
    assert Role.__tablename__ == "roles"
    assert_column_set(
        Role,
        ["id", "name", "description", "is_system_role"],
    )


def test_user_model_has_expected_columns():
    assert User.__tablename__ == "users"
    assert_column_set(
        User,
        [
            "id",
            "email",
            "username",
            "full_name",
            "_password_hash",
            "bio",
            "profile_pic_url",
            "contact_number",
            "x_user",
            "discord_user",
            "twitch_tv_user",
            "xbox_user",
            "steam_user",
            "epic_games_user",
            "battle_net_user",
            "riot_games_user",
            "created_at",
            "updated_at",
        ],
    )


def test_user_role_and_event_foreign_keys(setup_db):
    assert UserRole.__tablename__ == "user_roles"
    assert_column_set(UserRole, ["id", "user_id", "role_id"])
    assert_foreign_key(UserRole, "user_id", "users.id")
    assert_foreign_key(UserRole, "role_id", "roles.id")

    assert Event.__tablename__ == "events"
    assert_column_set(
        Event,
        [
            "id",
            "name",
            "start",
            "end",
            "in_person",
            "location",
            "description",
            "tie_breaking_rule",
            "created_at",
            "host_id",
        ],
    )
    assert_foreign_key(Event, "host_id", "users.id")


def test_tournament_and_match_tables_are_defined():
    assert Tournament.__tablename__ == "tournaments"
    assert_column_set(
        Tournament,
        [
            "id",
            "name",
            "start_time",
            "registration_deadline",
            "game",
            "platform",
            "line_up_type",
            "event_id",
        ],
    )
    assert_foreign_key(Tournament, "event_id", "events.id")

    assert Match.__tablename__ == "matches"
    assert_column_set(
        Match,
        ["id", "round", "start_time", "status", "tournament_id", "winner_id"],
    )
    assert_foreign_key(Match, "tournament_id", "tournaments.id")
    assert_foreign_key(Match, "winner_id", "tournament_competitors.id")
    assert Match.winner.property.mapper.class_ is TournamentCompetitor


def test_competitor_and_standing_tables_are_defined():
    assert TournamentCompetitor.__tablename__ == "tournament_competitors"
    assert_column_set(TournamentCompetitor, ["id", "user_id", "tournament_id"])
    assert_foreign_key(TournamentCompetitor, "user_id", "users.id")
    assert_foreign_key(TournamentCompetitor, "tournament_id", "tournaments.id")

    assert Player.__tablename__ == "players"
    assert_column_set(Player, ["id", "competitor_id", "match_id"])
    assert_foreign_key(Player, "competitor_id", "tournament_competitors.id")
    assert_foreign_key(Player, "match_id", "matches.id")

    assert Standing.__tablename__ == "standings"
    assert_column_set(Standing, ["id", "competitor_id", "points", "tournament_id"])
    assert_foreign_key(Standing, "competitor_id", "tournament_competitors.id")
    assert_foreign_key(Standing, "tournament_id", "tournaments.id")


def test_event_attendance_and_bracket_tables_are_defined():
    assert EventAttendee.__tablename__ == "event_attendees"
    assert_column_set(EventAttendee, ["id", "user_id", "event_id"])
    assert_foreign_key(EventAttendee, "user_id", "users.id")
    assert_foreign_key(EventAttendee, "event_id", "events.id")

    assert Bracket.__tablename__ == "brackets"
    assert_column_set(Bracket, ["id", "url", "tournament_id"])
    assert_foreign_key(Bracket, "tournament_id", "tournaments.id")


def test_primary_relationships_match_the_erd(setup_db):
    assert User.roles.property.mapper.class_ is UserRole
    assert UserRole.user.property.mapper.class_ is User
    assert UserRole.role.property.mapper.class_ is Role
    assert Role.users.property.mapper.class_ is UserRole

    assert User.hosted_events.property.mapper.class_ is Event
    assert Event.host.property.mapper.class_ is User
    assert Event.attendees.property.mapper.class_ is EventAttendee
    assert EventAttendee.event.property.mapper.class_ is Event
    assert EventAttendee.user.property.mapper.class_ is User

    assert Tournament.event.property.mapper.class_ is Event
    assert Event.tournaments.property.mapper.class_ is Tournament
    assert Tournament.competitors.property.mapper.class_ is TournamentCompetitor
    assert Tournament.matches.property.mapper.class_ is Match
    assert Tournament.standings.property.mapper.class_ is Standing
    assert Tournament.bracket.property.mapper.class_ is Bracket

    assert TournamentCompetitor.user.property.mapper.class_ is User
    assert TournamentCompetitor.tournament.property.mapper.class_ is Tournament
    assert TournamentCompetitor.players.property.mapper.class_ is Player
    assert Player.competitor.property.mapper.class_ is TournamentCompetitor
    assert Player.match.property.mapper.class_ is Match
    assert Standing.competitor.property.mapper.class_ is TournamentCompetitor
    assert Standing.tournament.property.mapper.class_ is Tournament
