from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from app.core.repositories.admin_user_management import AdminUserManagementInterface
from app.core.entities.admin_user_management import (
    TravellerEntity,
    GuideEntity,
    HostEntity,
    UserDetailsEntity,
)
from app.infrastructure.database.models.users.user import User as UserModel
from app.infrastructure.database.models.onboard import Guide, Host
from app.infrastructure.database.models.users.user import UserKyc
from app.core.enums import KycVerificationStatus
import logging

logger = logging.getLogger(__name__)

class AdminUserManagementImpl(AdminUserManagementInterface):
    """Implementation of admin user management repository"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_travellers(self) -> List[TravellerEntity]:
        """Get all travellers"""
        try:
            query = (
                select(UserModel)
                .where(
                    and_(
                        UserModel.is_traveller == True,
                        UserModel.is_active == True
                    )
                )
                .order_by(UserModel.created_at.desc())
            )
            result = await self.session.execute(query)
            users = result.scalars().all()
            
            travellers = []
            for user in users:
                # Get verification status from KYC
                kyc_query = select(UserKyc).where(UserKyc.user_id == user.id)
                kyc_result = await self.session.execute(kyc_query)
                kyc = kyc_result.scalar_one_or_none()
                
                status = "verified" if kyc and kyc.verification_status == KycVerificationStatus.ACCEPTED else "pending"
                
                traveller = TravellerEntity(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name or "",
                    email=user.email,
                    phone_number=user.phone_number,
                    is_verified=bool(kyc and kyc.verification_status == KycVerificationStatus.ACCEPTED),
                    is_active=user.is_active,
                    created_at=user.created_at,
                    last_login=None,  # Add last_login field to User model if needed
                    profile_image_url=user.profile_image,
                    status=status
                )
                travellers.append(traveller)
            
            logger.info(f"Retrieved {len(travellers)} travellers")
            return travellers
            
        except Exception as e:
            logger.error(f"Error getting travellers: {str(e)}")
            raise
    
    async def get_guides(self) -> List[GuideEntity]:
        """Get all guides"""
        try:
            query = (
                select(UserModel, Guide)
                .join(Guide, Guide.user_id == UserModel.id)
                .where(
                    and_(
                        UserModel.is_guide == True,
                        UserModel.is_active == True
                    )
                )
                .order_by(UserModel.created_at.desc())
            )
            result = await self.session.execute(query)
            rows = result.all()
            
            guides = []
            for user, guide in rows:
                # Get verification status from KYC
                kyc_query = select(UserKyc).where(UserKyc.user_id == user.id)
                kyc_result = await self.session.execute(kyc_query)
                kyc = kyc_result.scalar_one_or_none()
                
                status = "verified" if kyc and kyc.verification_status == KycVerificationStatus.ACCEPTED else "pending"
                
                guide_entity = GuideEntity(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name or "",
                    email=user.email,
                    phone_number=user.phone_number,
                    is_verified=bool(kyc and kyc.verification_status == KycVerificationStatus.ACCEPTED),
                    is_active=user.is_active,
                    created_at=user.created_at,
                    last_login=None,  # Add last_login field to User model if needed
                    profile_image_url=user.profile_image,
                    status=status,
                    is_guide_blocked=guide.is_blocked,
                    guide_rating=None,  # Add rating system if needed
                    total_tours=0  # Add tour count if needed
                )
                guides.append(guide_entity)
            
            logger.info(f"Retrieved {len(guides)} guides")
            return guides
            
        except Exception as e:
            logger.error(f"Error getting guides: {str(e)}")
            raise
    
    async def get_hosts(self) -> List[HostEntity]:
        """Get all hosts"""
        try:
            query = (
                select(UserModel, Host)
                .join(Host, Host.user_id == UserModel.id)
                .where(
                    and_(
                        UserModel.is_host == True,
                        UserModel.is_active == True
                    )
                )
                .order_by(UserModel.created_at.desc())
            )
            result = await self.session.execute(query)
            rows = result.all()
            
            hosts = []
            for user, host in rows:
                # Get verification status from KYC
                kyc_query = select(UserKyc).where(UserKyc.user_id == user.id)
                kyc_result = await self.session.execute(kyc_query)
                kyc = kyc_result.scalar_one_or_none()
                
                status = "verified" if kyc and kyc.verification_status == KycVerificationStatus.ACCEPTED else "pending"
                
                # Count properties for this host
                from app.infrastructure.database.models.onboard import Property
                property_query = select(Property).where(Property.host_id == user.id)
                property_result = await self.session.execute(property_query)
                properties = property_result.scalars().all()
                
                host_entity = HostEntity(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name or "",
                    email=user.email,
                    phone_number=user.phone_number,
                    is_verified=bool(kyc and kyc.verification_status == KycVerificationStatus.ACCEPTED),
                    is_active=user.is_active,
                    created_at=user.created_at,
                    last_login=None,  # Add last_login field to User model if needed
                    profile_image_url=user.profile_image,
                    status=status,
                    is_host_blocked=host.is_blocked,
                    total_properties=len(properties),
                    host_rating=None  # Add rating system if needed
                )
                hosts.append(host_entity)
            
            logger.info(f"Retrieved {len(hosts)} hosts")
            return hosts
            
        except Exception as e:
            logger.error(f"Error getting hosts: {str(e)}")
            raise
    
    async def get_user_details(self, user_id: int) -> Optional[UserDetailsEntity]:
        """Get detailed user information by ID"""
        try:
            query = (
                select(UserModel, Guide.is_blocked.label('guide_is_blocked'), Host.is_blocked.label('host_is_blocked'))
                .outerjoin(Guide, Guide.user_id == UserModel.id)
                .outerjoin(Host, Host.user_id == UserModel.id)
                .where(UserModel.id == user_id)
            )
            result = await self.session.execute(query)
            row = result.first()
            
            if not row:
                return None
            
            user, guide_is_blocked, host_is_blocked = row
            
            # Get verification status from KYC
            kyc_query = select(UserKyc).where(UserKyc.user_id == user.id)
            kyc_result = await self.session.execute(kyc_query)
            kyc = kyc_result.scalar_one_or_none()
            
            # Build roles list
            roles = []
            if user.is_traveller:
                roles.append("traveller")
            if user.is_guide:
                roles.append("guide")
            if user.is_host:
                roles.append("host")
            if user.is_admin:
                roles.append("admin")
            
            user_details = UserDetailsEntity(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name or "",
                email=user.email,
                phone_number=user.phone_number,
                is_verified=bool(kyc and kyc.verification_status == "accepted"),
                is_active=user.is_active,
                created_at=user.created_at,
                last_login=None,  # Add last_login field to User model if needed
                profile_image_url=user.profile_image,
                roles=roles,
                is_admin=user.is_admin,
                is_host=user.is_host,
                is_guide=user.is_guide,
                is_traveller=user.is_traveller,
                is_host_blocked=host_is_blocked or False,
                is_guide_blocked=guide_is_blocked or False
            )
            
            logger.info(f"Retrieved user details for user {user_id}")
            return user_details
            
        except Exception as e:
            logger.error(f"Error getting user details for user {user_id}: {str(e)}")
            raise
    
    async def deactivate_traveller(self, user_id: int) -> bool:
        """Deactivate traveller account"""
        try:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            
            if not user:
                return False
            
            user.is_active = False
            await self.session.commit()
            
            logger.info(f"Deactivated traveller {user_id}")
            return True
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error deactivating traveller {user_id}: {str(e)}")
            raise
    
    async def remove_host_privileges(self, user_id: int) -> bool:
        """Remove host privileges from user"""
        try:
            # Update user table
            query = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            
            if not user:
                return False
            
            user.is_host = False
            
            # Block the host profile
            host_query = select(Host).where(Host.user_id == user_id)
            host_result = await self.session.execute(host_query)
            host = host_result.scalar_one_or_none()
            
            if host:
                host.is_blocked = True
            
            await self.session.commit()
            
            logger.info(f"Removed host privileges for user {user_id}")
            return True
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error removing host privileges for user {user_id}: {str(e)}")
            raise
    
    async def remove_guide_privileges(self, user_id: int) -> bool:
        """Remove guide privileges from user"""
        try:
            # Update user table
            query = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            
            if not user:
                return False
            
            user.is_guide = False
            
            # Block the guide profile
            guide_query = select(Guide).where(Guide.user_id == user_id)
            guide_result = await self.session.execute(guide_query)
            guide = guide_result.scalar_one_or_none()
            
            if guide:
                guide.is_blocked = True
            
            await self.session.commit()
            
            logger.info(f"Removed guide privileges for user {user_id}")
            return True
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error removing guide privileges for user {user_id}: {str(e)}")
            raise
    
    
    async def reactivate_traveller(self, user_id: int) -> bool:
        """Reactivate traveller account"""
        try:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            
            if not user:
                return False
            
            user.is_active = True
            await self.session.commit()
            
            logger.info(f"Reactivated traveller {user_id}")
            return True
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error reactivating traveller {user_id}: {str(e)}")
            raise
    
    async def reinstate_host_privileges(self, user_id: int) -> bool:
        """Reinstate host privileges for user"""
        try:
            # Update user table
            query = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            
            if not user:
                return False
            
            user.is_host = True
            
            # Unblock the host profile
            host_query = select(Host).where(Host.user_id == user_id)
            host_result = await self.session.execute(host_query)
            host = host_result.scalar_one_or_none()
            
            if host:
                host.is_blocked = False
            
            await self.session.commit()
            
            logger.info(f"Reinstated host privileges for user {user_id}")
            return True
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error reinstating host privileges for user {user_id}: {str(e)}")
            raise
    
    async def reinstate_guide_privileges(self, user_id: int) -> bool:
        """Reinstate guide privileges for user"""
        try:
            # Update user table
            query = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            
            if not user:
                return False
            
            user.is_guide = True
            
            # Unblock the guide profile
            guide_query = select(Guide).where(Guide.user_id == user_id)
            guide_result = await self.session.execute(guide_query)
            guide = guide_result.scalar_one_or_none()
            
            if guide:
                guide.is_blocked = False
            
            await self.session.commit()
            
            logger.info(f"Reinstated guide privileges for user {user_id}")
            return True
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error reinstating guide privileges for user {user_id}: {str(e)}")
            raise
