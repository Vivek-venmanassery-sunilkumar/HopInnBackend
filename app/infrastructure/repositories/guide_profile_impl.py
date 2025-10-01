from app.core.repositories import GuideProfileInterface
from app.core.entities import GuideOnboardEntity
from app.api.schemas import GuideProfileSchema, AddressSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models.onboard import Guide, Languages
from sqlalchemy.future import select
from sqlalchemy import update, delete, insert
from sqlalchemy.exc import SQLAlchemyError
from geoalchemy2.shape import to_shape
from geoalchemy2 import WKTElement
from typing import Optional

import logging
logger = logging.getLogger(__name__) 

class GuideProfileImpl(GuideProfileInterface):
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session
    
    async def get(self, user_id: str)->Optional[GuideProfileSchema]:
        profile_data = await self.session.scalar(
            select(Guide).where(Guide.user_id == int(user_id))
        )

        if not profile_data:
            return

        languages_result = await self.session.scalars(
            select(Languages.language).where(Languages.user_id == int(user_id))
        )
        known_languages = languages_result.all()
        coordinates = {}
        if profile_data.location:
            point = to_shape(profile_data.location)
            coordinates={"lat": point.y, "lon": point.x}

        address_data = AddressSchema(
            houseName=profile_data.house_name,
            landmark=profile_data.landmark,
            pincode=profile_data.pincode,
            district=profile_data.district,
            state=profile_data.state,
            country=profile_data.country,
            coordinates=coordinates
        )

        return GuideProfileSchema(
            bio=profile_data.bio,
            profession=profile_data.profession,
            hourlyRate=profile_data.hourly_rate,
            expertise=profile_data.expertise,
            address=address_data,
            knownLanguages=known_languages,
            joinedOn = profile_data.created_at.date(),
        )

    async def update_profile(self, user_id: str, guide_data: GuideOnboardEntity)->bool:
        logger.info("I am inside the update profile function in the guideprofileimplementation")
        try:
            guide_update_stmt = (
                update(Guide)
                .where(Guide.user_id == int(user_id))
                .values(
                    bio=guide_data.about,
                    profession=guide_data.profession,
                    expertise=guide_data.expertise,
                    hourly_rate=guide_data.hourly_rate,
                    landmark=guide_data.landmark,
                    pincode=guide_data.pincode,
                    district=guide_data.district,
                    state=guide_data.state,
                    country=guide_data.country,
                    location=WKTElement(f'POINT({guide_data.coordinates['lon']} {guide_data.coordinates['lat']})', srid=4326) 
                    if guide_data.coordinates and 'lat' in guide_data.coordinates and 
                    'lon' in guide_data.coordinates else None
                )
            )

            await self.session.execute(guide_update_stmt)

            delete_languages_stmt = (
                delete(Languages)
                .where(Languages.user_id == int(user_id))
            )
            await self.session.execute(delete_languages_stmt)

            if guide_data.known_languages:
                languages_data = [
                    {'user_id': int(user_id), 'language': lang}
                    for lang in guide_data.known_languages
                ]


                await self.session.execute(insert(Languages).values(languages_data))
            
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            return False