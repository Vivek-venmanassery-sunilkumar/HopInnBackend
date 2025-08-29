from app.infrastructure.repositories import SQLAlchemyUserRepository
from app.infrastructure.database.session import SessionLocal

async def get_cli_user_repository():
    """Create a session directly for CLI use"""
    session = SessionLocal()
    return SQLAlchemyUserRepository(session=session)