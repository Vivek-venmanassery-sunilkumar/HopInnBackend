from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.core.repositories.user_management_repo_interface import UserManagementRepoInterface
from app.core.entities.user_management_entity import TravellerUserEntity, GuideUserEntity, HostUserEntity
from app.infrastructure.database.models.users.user import User
from app.infrastructure.database.models.onboard import Guide, Host


class UserManagementRepoImpl(UserManagementRepoInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_travellers(self) -> List[TravellerUserEntity]:
        query = select(User).where(
            User.is_traveller == True,
            User.is_admin == False
        )
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        return [
            TravellerUserEntity(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone_number=user.phone_number,
                dob=user.dob.isoformat() if user.dob else None,
                is_active=user.is_active,
                created_at=user.created_at
            )
            for user in users
        ]

    async def get_guides(self) -> List[GuideUserEntity]:
        query = select(User, Guide).join(Guide, User.id == Guide.user_id).where(
            User.is_guide == True
        )
        result = await self.db.execute(query)
        rows = result.all()
        
        return [
            GuideUserEntity(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone_number=user.phone_number,
                district=guide.district,
                country=guide.country,
                is_blocked=guide.is_blocked,
                is_active=user.is_active,
                created_at=guide.created_at
            )
            for user, guide in rows
        ]

    async def get_hosts(self) -> List[HostUserEntity]:
        query = select(User, Host).join(Host, User.id == Host.user_id).where(
            User.is_host == True
        )
        result = await self.db.execute(query)
        rows = result.all()
        
        return [
            HostUserEntity(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone_number=user.phone_number,
                is_blocked=host.is_blocked,
                is_active=user.is_active,
                created_at=host.created_at
            )
            for user, host in rows
        ]

    async def update_traveller_status(self, email: str, is_active: bool) -> Dict[str, Any]:
        """
        Update traveller status (is_active in User model)
        If blocking traveller, also block their guide and host privileges
        """
        # First, get the user
        user_query = select(User).where(User.email == email)
        user_result = await self.db.execute(user_query)
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise ValueError(f"User with email {email} not found")
        
        # Update user is_active status
        user_update_query = update(User).where(User.email == email).values(is_active=is_active)
        await self.db.execute(user_update_query)
        
        # If blocking the user, also block their guide and host privileges
        if not is_active:
            # Block guide privileges if user is a guide
            if user.is_guide:
                guide_update_query = update(Guide).where(Guide.user_id == user.id).values(is_blocked=True)
                await self.db.execute(guide_update_query)
            
            # Block host privileges if user is a host
            if user.is_host:
                host_update_query = update(Host).where(Host.user_id == user.id).values(is_blocked=True)
                await self.db.execute(host_update_query)
        
        await self.db.commit()
        
        return {
            "email": email,
            "is_active": is_active,
            "message": "Traveller status updated successfully"
        }

    async def update_guide_status(self, email: str, is_blocked: bool) -> Dict[str, Any]:
        """
        Update guide status (is_blocked in Guide model)
        If unblocking guide, check if user is active first
        """
        # First, get the user and guide
        query = select(User, Guide).join(Guide, User.id == Guide.user_id).where(User.email == email)
        result = await self.db.execute(query)
        row = result.first()
        
        if not row:
            raise ValueError(f"Guide with email {email} not found")
        
        user, guide = row
        
        # If trying to unblock guide, check if user is active
        if not is_blocked and not user.is_active:
            raise ValueError(f"Cannot unblock guide privileges for inactive user {email}. User account must be active first.")
        
        # Update guide is_blocked status
        guide_update_query = update(Guide).where(Guide.user_id == user.id).values(is_blocked=is_blocked)
        await self.db.execute(guide_update_query)
        
        await self.db.commit()
        
        return {
            "email": email,
            "is_blocked": is_blocked,
            "message": "Guide status updated successfully"
        }

    async def update_host_status(self, email: str, is_blocked: bool) -> Dict[str, Any]:
        """
        Update host status (is_blocked in Host model)
        If unblocking host, check if user is active first
        """
        # First, get the user and host
        query = select(User, Host).join(Host, User.id == Host.user_id).where(User.email == email)
        result = await self.db.execute(query)
        row = result.first()
        
        if not row:
            raise ValueError(f"Host with email {email} not found")
        
        user, host = row
        
        # If trying to unblock host, check if user is active
        if not is_blocked and not user.is_active:
            raise ValueError(f"Cannot unblock host privileges for inactive user {email}. User account must be active first.")
        
        # Update host is_blocked status
        host_update_query = update(Host).where(Host.user_id == user.id).values(is_blocked=is_blocked)
        await self.db.execute(host_update_query)
        
        await self.db.commit()
        
        return {
            "email": email,
            "is_blocked": is_blocked,
            "message": "Host status updated successfully"
        }
