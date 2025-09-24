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
    logger.info(f'user_id: {user_id}')

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
            detail='Account has been deactivated'
        )


async def verify_admin(
        request: Request,
        user_roles_permissions_repo: UserRolesPermissionsInterface = Depends(get_user_roles_permissions)
):
    user_id = getattr(request.state, 'user_id', None)
    logger.info(f'user_id: {user_id}')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication required'
        )
    user_roles_permissions = await user_roles_permissions_repo.get_user_roles_and_permissions(user_id)

    if not user_roles_permissions.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You dont have admin privileges'
        )

async def verify_guide(
        request: Request,
        user_roles_permissions_repo: UserRolesPermissionsInterface = Depends(get_user_roles_permissions)
):
    user_id = getattr(request.state, 'user_id', None)
    logger.info(f'user_id: {user_id}')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication required'
        )
    user_roles_permissions = await user_roles_permissions_repo.get_user_roles_and_permissions(user_id)

    if not user_roles_permissions.is_guide and not user_roles_permissions.is_guide_blocked:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail='You dont have guide privileges'
        )

async def verify_host(
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

    if not user_roles_permissions.is_host and not user_roles_permissions.is_host_blocked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You dont have host privileges'
        )
    
    