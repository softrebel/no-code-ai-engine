from beanie import Document, Link
from pydantic import BaseModel
from .user import User


class ModelInput(BaseModel):
    name: str
    description: str
    is_public: bool = False
    design_flow: dict
    report_flow: dict
    usage: int = 0
    last_modified: str = None


class ModelView(ModelInput):
    last_modified_at: int = 0
    created_at: int = 0


class Model(Document, ModelView):
    user: Link[User]

    class Settings:
        name = "model"
