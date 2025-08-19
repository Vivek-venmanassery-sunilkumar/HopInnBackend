from app.core.entities.user import User
from app.core.repositories.traveller.user_repository import UserRepository
from app.infrastructure.database.models.users.user import User as UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.api.schemas.Traveller.authentication import UserRegisterSchema
from app.api.schemas.roles.roles import UserRoles
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
            full_name = db_user.full_name,
            email = db_user.email,
            phone_number = db_user.phone_number,
            password_hash = db_user.password_hash,
            profile_image = db_user.profile_image,
            google_id = db_user.google_id,
            is_traveller = db_user.is_traveller,
            is_guide=db_user.is_guide,
            is_host = db_user.is_host,
            is_active = db_user.is_active,
            is_admin = db_user.is_admin,
            created_at = db_user.created_at,
            updated_at = db_user.updated_at
        )
    
    async def verify_password(self, password, hashed_password):
        return pwd_context.verify(password, hashed_password)

    async def get_user_roles(self, user_id: str)->UserRoles:
        db_user = await self.session.scalar(
            select(UserModel).where(UserModel.id == int(user_id))
        ) 

        if not db_user:
            return None
        
        return UserRoles(
            id=str(db_user.id),
            isTraveller=db_user.is_traveller,
            isGuide=db_user.is_guide,
            isHost = db_user.is_host,
            isAdmin=db_user.is_admin,
            isActive=db_user.is_active
        )

