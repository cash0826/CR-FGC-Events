from .base_controller import BaseController
from services.brackets_service import BracketService
from schemas.bracket_schema import BracketSchema

class BracketsController(BaseController):
    service = BracketService
    schema = BracketSchema()
