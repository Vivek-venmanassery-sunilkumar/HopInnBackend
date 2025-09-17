from app.core.repositories import OnboardRepo
from app.core.entities import GuideOnboardEntity, HostOnboardEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update, delete, insert
from sqlalchemy.future import select
from app.infrastructure.database.models.onboard import Guide, Languages, Host, PropertyImages, Property, PropertyAddress, PropertyAmenities 
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

            await self.session.execute(
                delete(Languages)
                .where(Languages.user_id == int(user_id))
            )
            for lang in data.known_languages:
                db_language = Languages(
                    user_id = int(user_id),
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

    async def onboard_host(self, data: HostOnboardEntity, user_id: str) -> bool: 
        try:
            # Remove the context manager and use manual management like guide
            host_insert_query = insert(Host).values(
                user_id=int(user_id),
                about=data.about,
                dob=data.dob,
                profession=data.profession,
            ).returning(Host.id)

            host_result = await self.session.execute(host_insert_query)
            host_id = host_result.scalar_one()

            property_insert_query = insert(Property).values(
                host_id=host_id,
                property_name=data.property_name,
                property_type=data.property_type,
                property_description=data.property_description,
            ).returning(Property.id)

            property_result = await self.session.execute(property_insert_query)
            property_id = property_result.scalar_one()

            coordinates = data.property_address.coordinates
            point = None
            if coordinates and 'longitude' in coordinates and 'latitude' in coordinates:    
                point = f"POINT({coordinates['longitude']} {coordinates['latitude']})"
            
            address_insert_query = insert(PropertyAddress).values(
                property_id=property_id,
                house_name=data.property_address.house_name,  
                landmark=data.property_address.landmark,
                pincode=data.property_address.pincode,   
                district=data.property_address.district,
                state=data.property_address.state,
                country=data.property_address.country,
                location=point
            )
            await self.session.execute(address_insert_query)

            for img in data.property_images:
                image_insert_query = insert(PropertyImages).values(
                    property_id=property_id,
                    image_url=img.image_url,
                    is_primary=img.is_primary,
                    public_id=img.public_id
                )
                await self.session.execute(image_insert_query)
            
            for amenity in data.amenities:
                amenity_insert_query = insert(PropertyAmenities).values(
                    property_id=property_id,
                    amenity=amenity
                )
                await self.session.execute(amenity_insert_query)
            
            # Delete existing languages
            await self.session.execute(
                delete(Languages).where(Languages.user_id == int(user_id))
            )
            
            # Add new languages
            for lang in data.known_languages:
                db_language = Languages(
                    user_id=int(user_id),
                    language=lang.strip()
                )
                self.session.add(db_language)
            
            # MANUAL COMMIT like in guide onboarding
            await self.session.commit()
            return True
            
        except Exception as e:
            # MANUAL ROLLBACK like in guide onboarding
            await self.session.rollback()
            logger.info(f'Error onboarding host: {e}')
            return False

    async def update_user_to_host(self, user_id: str) -> bool:
        try:
            logger.info(f"Updating user_id: {user_id} to host")
            
            # Remove context manager, use manual like guide
            query = (
                update(UserModel)
                .where(UserModel.id == int(user_id))
                .values(is_host=True)
            )
            
            logger.info(f"DEBUG: Executing update query")
            result = await self.session.execute(query)
            logger.info(f"DEBUG: Rowcount: {result.rowcount}")

            if result.rowcount > 0:
                logger.info("DEBUG: Update successful, committing...")
                # MANUAL COMMIT
                await self.session.commit()
                return True
            else:
                # MANUAL ROLLBACK
                await self.session.rollback()
                return False
                
        except SQLAlchemyError as e:
            # MANUAL ROLLBACK
            await self.session.rollback()
            logger.error(f"SQLAlchemy error updating user to host: {e}")
            return False
        except Exception as e:
            # MANUAL ROLLBACK
            await self.session.rollback()
            logger.error(f"Unexpected error updating user to host: {e}")
            return False

    async def user_is_host(self, user_id: str)->bool:
        query=(
            select(UserModel)
            .where(UserModel.id == int(user_id))    
        )
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            return False
        return user.is_host