from app.core.entities.user import User
from app.core.repositories.traveller.user_repository import UserRepository
from app.infrastructure.database.models.users.user import User as UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.api.schemas.Traveller.authentication import UserRegisterSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

log = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_user(self, user_data: UserRegisterSchema) -> bool:
        hashed_password = pwd_context.hash(user_data.password)

        try:
            db_user = UserModel(
                full_name = user_data.fullName,
                email = user_data.email,
                phone_number = user_data.phoneNumber,
                password_hash = hashed_password,
                is_traveller = True
            )

            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            log.info("User created successfully: %s", db_user.email)
            return True
        except IntegrityError as e:
            await self.session.rollback()
            log.warning("User already exists: %s", user_data.email)
            return False
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.exception("Database error occured while creating user")
            return False
    
    async def get_user_by_email(self, email: str)-> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        db_user = result.scalars().first()

        if not db_user:
            return None
        
        return User(
            id=str(db_user.id),
            fullName = db_user.full_name,
            email = db_user.email,
            phoneNumber = db_user.phone_number,
            passwordHash = db_user.password_hash,
            isTraveller = db_user.is_traveller
        )
        