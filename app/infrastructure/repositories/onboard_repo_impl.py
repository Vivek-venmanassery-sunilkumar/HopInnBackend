from app.core.repositories import OnboardRepo
from app.core.entities import GuideOnboardEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update
from sqlalchemy.future import select
from app.infrastructure.database.models.onboard import Guide, Languages
from app.infrastructure.database.models.users.user import User as UserModel
import logging

logger = logging.getLogger(__name__)


class OnboardRepoImpl(OnboardRepo):
    def __init__(
            self,
            session:AsyncSession
        ):
        self.session = session
    
    async def onboard_guide(self, data: GuideOnboardEntity, user_id: str)->bool:
        try:
            location = None
            if data.coordinates and 'longitude' in data.coordinates and 'latitude' in data.coordinates:
                lon = data.coordinates['longitude']
                lat = data.coordinates['latitude']
                location = f'POINT({lon} {lat})'

            db_guide = Guide(
                user_id = int(user_id),
                bio = data.about,
                dob = data.dob,
                profession = data.profession,
                hourly_rate = data.hourly_rate,
                expertise = data.expertise,
                house_name = data.house_name,
                landmark = data.landmark,
                pincode = data.pincode,
                state = data.state,
                district = data.district,
                country = data.country,
                location=location
            )

            self.session.add(db_guide)
            await self.session.flush()

            for lang in data.known_languages:
                db_language = Languages(
                    guide_id = db_guide.id,
                    language=lang.strip()
                )

                self.session.add(db_language)
            
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logger.info(f'Error onboarding guide: {e}')
            return False
            
    async def update_user_to_guide(self, user_id: str)->bool:
        try:
            logger.info(f"Updating user_id: {user_id} to guide ")

            user_exists_query = select(UserModel.id).where(UserModel.id== int(user_id))
            user_exists = await self.session.scalar(user_exists_query)

            #First 
            query=(
                update(UserModel)
                .where(UserModel.id==int(user_id))
                .values(is_guide=True)
            )
            logger.info(f"DEBUG: Executing update query")
            result = await self.session.execute(query)
            logger.info(f"DEBUG: Rowcount: {result.rowcount}")

            if result.rowcount>0:
                logger.info("DEBUG: Update successfull, committing...")
                await self.session.commit()
                return True
            else:
                await self.session.rollback()
                return False
        except SQLAlchemyError as e:
            await self.session.rollback()
            return False
        except Exception as e:
            await self.session.rollback()
            return False
        
    async def user_is_guide(self, user_id: str)->bool:
        query=(
            select(UserModel)
            .where(UserModel.id == int(user_id))    
        )
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            return False
        return user.is_guide
