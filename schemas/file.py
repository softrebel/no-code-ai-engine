from beanie import Document,Link
from .user import User

class File(Document):
    filename: str
    original_filename:str
    content_type: str
    path: str
    user:Link[User]

    class Settings:
        name = "file"
