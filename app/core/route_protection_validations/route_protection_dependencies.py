from app.core.repositories import UserRolesPermissionsInterface
from fastapi import Request,status,HTTPException, Depends
from app.api.dependencies import get_user_roles_permissions
import logging

logger = logging.getLogger(__name__)

async def verify_traveller(
        request: Request,
        user_roles_permissions_repo: UserRolesPermissionsInterface = Depends(get_user_roles_permissions)
):
    user_id = getattr(request.state, 'user_id', None)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication required'
        )
    
    user_roles_permissions = await user_roles_permissions_repo.get_user_roles_and_permissions(user_id)
    logger.info(user_roles_permissions)

    if not user_roles_permissions.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detiail='Account has been deactivated'
        )