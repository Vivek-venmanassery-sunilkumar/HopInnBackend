from app.core.entities import UserEntity, AdminCreationEntity, GoogleSettingsEntity
from app.core.repositories import UserRepository
from app.infrastructure.database.models.users.user import User as UserModel
from app.infrastructure.database.models.onboard import Guide,Host
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.api.schemas import UserRegisterSchema, UserRolesSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from google.oauth2 import id_token
from google.auth.transport import requests
import logging

log = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

class SQLAlchemyUserRepository(UserRepository):
    def __init__(
            self, 
            session: AsyncSession,
            google_client:GoogleSettingsEntity
        ):
        self.session = session
        self.google_client = google_client
    
    def __hash_password(self, password: str):
        return pwd_context.hash(password)

    async def create_user(self, user_data: UserRegisterSchema) -> bool:
        hashed_password = self.__hash_password(user_data.password)

        try:
            db_user = UserModel(
                first_name = user_data.firstName,
                last_name = user_data.lastName,
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
    
    async def get_user_by_email(self, email: str)-> UserEntity | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        db_user = result.scalars().first()

        if not db_user:
            return None
        
        return UserEntity(
            id=str(db_user.id),
            first_name = db_user.first_name,
            last_name = db_user.last_name,
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

    async def get_user_roles(self, user_id: str)->UserRolesSchema:
        query = (
            select(UserModel, Guide.is_blocked.label('guide_is_blocked'), Host.is_blocked.label('host_is_blocked'))
            .outerjoin(Guide, Guide.user_id == UserModel.id)
            .outerjoin(Host, Host.user_id == UserModel.id)
            .where(UserModel.id == int(user_id))
        )
        result = await self.session.execute(query)
        row = result.first()
        db_user, guide_is_blocked, host_is_blocked = row 

        return UserRolesSchema(
            id=str(db_user.id),
            isTraveller=db_user.is_traveller,
            isGuide=db_user.is_guide,
            isGuideBlocked=guide_is_blocked if guide_is_blocked is not None else False,
            isHost = db_user.is_host,
            isHostBlocked=host_is_blocked if host_is_blocked is not None else False,
            isAdmin=db_user.is_admin,
            isActive=db_user.is_active,
        )
    
    async def create_admin_user(self, admin_data: AdminCreationEntity)->bool:
        hashed_password = self.__hash_password(admin_data.password)

        try:
            db_admin_user = UserModel(
                first_name = admin_data.first_name,
                last_name = admin_data.last_name,
                email = admin_data.email,
                password_hash = hashed_password,
                is_admin = True
            )

            self.session.add(db_admin_user)
            await self.session.commit()
            await self.session.refresh(db_admin_user)
            return True
        except IntegrityError as e:
            await self.session.rollback() 
            log.warning('This admin user already exists')
            return False
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.warning(f"Some database error occured while creating admin user")
            return False
        
    async def does_user_exist(self, email:str)->bool:
        result = await self.session.scalar(
            select(UserModel).where(UserModel.email == email)
        )

        return result is not None
    
    async def verify_google_token(self, google_token: str)-> dict:
        idinfo = id_token.verify_oauth2_token(
            google_token,
            requests.Request(),
            self.google_client.CLIENT_ID
        )
        return idinfo
    
    async def update_google_user_info(self, email: str, google_id: str, picture: str)->bool:
        """Update user's google information"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )

        db_user = result.scalars().first()
        if db_user:
            db_user.google_id = google_id
            db_user.profile_image = picture
            await self.session.commit()
            return True
        return False
    
    async def create_google_user(self, email: str, name: str, google_id: str, picture: str)->bool:
        try:
            db_user = UserModel(
                first_name = name.split(' ')[0],
                last_name = " ".join(name.split(" ")[1:]) if len(name.split(" ")) > 1 else "",
                email=email,
                google_id=google_id,
                profile_image = picture,
                is_traveller=True
            )

            self.session.add(db_user)
            await self.session.commit()
            return True
        except Exception:
            return False
