from .base_controller import BaseController
from services.players_service import PlayerService
from schemas.player_schema import PlayerSchema

class Controller(BaseController):
    service = PlayerService
    schema = PlayerSchema()