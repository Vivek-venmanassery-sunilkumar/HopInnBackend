from app.core.repositories import KycRepo, OnboardRepo, PropertyRepo
from app.core.entities import HostOnboardEntity, HostEntity, PropertyDetailsEntity, GuideOnboardEntity
from app.core.exceptions import KycNotAcceptedError
import logging


logger = logging.getLogger(__name__)


class OnBoardingUseCase:
    def __init__(
        self,
        kyc_repo: KycRepo,
        onboard_repo: OnboardRepo,
        property_repo: PropertyRepo | None = None
    ):
        self.kyc_repo = kyc_repo
        self.onboard_repo = onboard_repo
        self.property_repo = property_repo
    
    async def onboard_guide(self, data: GuideOnboardEntity, user_id: str)->bool:
        try:
            kyc_accepted = await self.kyc_repo.check_kyc_accepted(user_id)
            if not kyc_accepted:
                raise KycNotAcceptedError

            user_is_guide = await self.onboard_repo.user_is_guide(user_id)
            if user_is_guide:
                return True

            guide_onboarded = await self.onboard_repo.onboard_guide(data, user_id)

            if not guide_onboarded:
                return False
            updated = await self.onboard_repo.update_user_to_guide(user_id)
            return updated
        except KycNotAcceptedError:
            raise
        
        except Exception as e:
            logger.error(f"Error in guide onboarding for user {user_id}: {e}")
            return False
    
    async def onboard_host(self, user_id: str, data: HostOnboardEntity)->bool:
        try:
            logger.info(f"Recieved data for host onboarding: {data}")
            logger.info(f"Known languages data: {data.known_languages}, type: {type(data.known_languages)}")
            kyc_accepted = await self.kyc_repo.check_kyc_accepted(user_id)
            if not kyc_accepted:
                raise KycNotAcceptedError

            user_is_host = await self.onboard_repo.user_is_host(user_id)
            if user_is_host:
                return True
            
            host_data = HostEntity(
                about=data.about,
                profession=data.profession, 
                known_languages = data.known_languages
            )
            
            host_id = await self.onboard_repo.add_host(data = host_data, user_id = user_id)
            logger.info(f"The host id that is created right now is: {host_id}")
            if not host_id:
                return False

            property_data =  PropertyDetailsEntity(
                host_id = host_id,
                property_name = data.property_name,
                property_description = data.property_description,
                property_type = data.property_type,
                property_address = data.property_address, 
                property_images = data.property_images, 
                amenities= data.amenities,
                max_guests = data.max_guests,
                bedrooms = data.bedrooms,
                price_per_night = data.price_per_night
            )
            
            property_id =await self.property_repo.add_property(property_data=property_data)
            if not property_id:
                return False

            updated = await self.onboard_repo.update_user_to_host(user_id)
            return updated
        except KycNotAcceptedError:
            raise
        except Exception as e:
            logger.error(f"Error in host onboarding for user {user_id}: {e}")
            return False