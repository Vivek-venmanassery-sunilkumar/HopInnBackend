from app.core.entities.user import User
from app.core.repositories.traveller.user_repository import UserRepository
from app.infrastructure.database.models.users.user import User as UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_user(self, user: User) -> User:
        hashed_password = pwd_context.hash(user.password_hash)

        db_user = UserModel(
            full_name = user.full_name,
            email = user.email,
            phone_number = user.phone_number,
            password_hash = hashed_password,
            is_traveller = True
        )

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return User(
            id=str(db_user.id),
            full_name = db_user.full_name,
            email = db_user.email,
            phone_number = db_user.phone_number,
            password_hash = db_user.password_hash,
            is_traveller = True
        )
    
    async def get_user_by_email(self, email: str)-> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        db_user = result.scalars().first()

        if not db_user:
            return None
        
        return User(
            id=str(db_user.id),
            full_name = db_user.full_name,
            email = db_user.email,
            phone_number = db_user.phone_number,
            password_hash = db_user.password_hash,
            is_traveller = db_user.is_traveller
        )
        