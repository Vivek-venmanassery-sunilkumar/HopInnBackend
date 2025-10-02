from app.core.repositories import HostProfileInterface
from app.api.schemas import HostProfileSchema
from app.core.entities import HostProfileUpdateEntity
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models.onboard import Host, Languages
from sqlalchemy.future import select
from sqlalchemy import update, delete, insert
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

    async def update_profile(self, user_id: str, update_data: HostProfileUpdateEntity) -> bool:
        """Update host profile with the given data"""
        try:
            user_id_int = int(user_id)
            
            # Update main host table if needed
            if update_data.has_about_update() or update_data.has_profession_update():
                await self._update_host_main_data(user_id_int, update_data)
            
            # Update languages if provided
            if update_data.has_languages_update():
                await self._update_host_languages(user_id_int, update_data.known_languages)
            
            await self.session.commit()
            logger.info(f"Successfully updated host profile for user {user_id}")
            return True
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error updating host profile for user {user_id}: {str(e)}")
            return False

    async def _update_host_main_data(self, user_id: int, update_data: HostProfileUpdateEntity):
        """Update the main host table fields"""
        update_fields = {}
        
        if update_data.has_about_update():
            update_fields['about'] = update_data.about
        
        if update_data.has_profession_update():
            update_fields['profession'] = update_data.profession
        
        if update_fields:
            host_update_query = update(Host).where(
                Host.user_id == user_id
            ).values(**update_fields)
            await self.session.execute(host_update_query)

    async def _update_host_languages(self, user_id: int, languages: list):
        """Update host languages by replacing all existing ones"""
        # Delete existing languages
        delete_languages_query = delete(Languages).where(
            Languages.user_id == user_id
        )
        await self.session.execute(delete_languages_query)
        
        # Insert new languages
        for language in languages:
            language_insert_query = insert(Languages).values(
                user_id=user_id,
                language=language
            )
            await self.session.execute(language_insert_query)
