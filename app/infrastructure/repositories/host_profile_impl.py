from app.core.repositories import HostProfileInterface
from app.api.schemas import HostProfileSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models.onboard import Host, Languages
from sqlalchemy.future import select
from typing import Optional

import logging
logger = logging.getLogger(__name__) 

class HostProfileImpl(HostProfileInterface):
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session
    
    async def get(self, user_id: str)->Optional[HostProfileSchema]:
        profile_data = await self.session.scalar(
            select(Host).where(Host.user_id == int(user_id))
        )

        if not profile_data:
            return

        languages_result = await self.session.scalars(
            select(Languages.language).where(Languages.user_id == int(user_id))
        )
        known_languages = languages_result.all()


        return HostProfileSchema(
            about=profile_data.about,
            profession=profile_data.profession,
            knownLanguages=known_languages,
            joinedOn = profile_data.created_at.date(),
        )
