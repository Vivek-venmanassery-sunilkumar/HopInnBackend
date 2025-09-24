from app.core.repositories import GuideProfileInterface
from app.api.schemas import GuideProfileSchema, AddressSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models.onboard import Guide, Languages
from sqlalchemy.future import select
from geoalchemy2.shape import to_shape
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
            hourly_rate=profile_data.hourly_rate,
            expertise=profile_data.expertise,
            address=address_data,
            knownLanguages=known_languages,
            joinedOn = profile_data.created_at.date(),
        )

        