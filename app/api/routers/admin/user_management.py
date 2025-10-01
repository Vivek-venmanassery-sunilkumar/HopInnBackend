from fastapi import APIRouter, Request, status, HTTPException, Depends
from app.core.route_protection_validations.route_protection_dependencies import verify_admin
from app.core.repositories.admin_user_management import AdminUserManagementInterface
from app.api.dependencies import AdminUserManagementDep
from app.core.use_cases.admin_user_management import AdminUserManagementUseCase
from app.api.schemas.admin.user_management import (
    UserListResponse,
    UserDetailsResponse,
    UserActionResponse,
    TravellerInfo,
    GuideInfo,
    HostInfo,
    UserDetails
)

router = APIRouter(prefix="/admin/users", tags=["Admin User Management"])

@router.get("/travellers", response_model=UserListResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def get_travellers(
    request: Request,
    admin_user_repo: AdminUserManagementDep
):
    """Get all travellers"""
    try:
        admin_uc = AdminUserManagementUseCase(admin_user_repo)
        travellers = await admin_uc.get_travellers()
        
        # Serialize users with camelCase aliases
        serialized_users = [user.model_dump(by_alias=True) for user in travellers]
        
        return {
            "success": True,
            "message": "Travellers fetched successfully",
            "users": serialized_users,
            "total_count": len(travellers)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching travellers: {str(e)}"
        )

@router.get("/guides", response_model=UserListResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def get_guides(
    request: Request,
    admin_user_repo: AdminUserManagementDep
):
    """Get all guides"""
    try:
        admin_uc = AdminUserManagementUseCase(admin_user_repo)
        guides = await admin_uc.get_guides()
        
        # Serialize users with camelCase aliases
        serialized_users = [user.model_dump(by_alias=True) for user in guides]
        
        return {
            "success": True,
            "message": "Guides fetched successfully",
            "users": serialized_users,
            "total_count": len(guides)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching guides: {str(e)}"
        )

@router.get("/hosts", response_model=UserListResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def get_hosts(
    request: Request,
    admin_user_repo: AdminUserManagementDep
):
    """Get all hosts"""
    try:
        admin_uc = AdminUserManagementUseCase(admin_user_repo)
        hosts = await admin_uc.get_hosts()
        
        # Serialize users with camelCase aliases
        serialized_users = [user.model_dump(by_alias=True) for user in hosts]
        
        return {
            "success": True,
            "message": "Hosts fetched successfully",
            "users": serialized_users,
            "total_count": len(hosts)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching hosts: {str(e)}"
        )

@router.get("/{user_id}", response_model=UserDetailsResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def get_user_details(
    user_id: int,
    request: Request,
    admin_user_repo: AdminUserManagementDep
):
    """Get specific user details"""
    try:
        admin_uc = AdminUserManagementUseCase(admin_user_repo)
        user = await admin_uc.get_user_details(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Serialize user with camelCase aliases
        serialized_user = user.model_dump(by_alias=True)
        
        return {
            "success": True,
            "message": "User details fetched successfully",
            "user": serialized_user
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user details: {str(e)}"
        )

@router.put("/travellers/{user_id}/deactivate", response_model=UserActionResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def deactivate_traveller(
    user_id: int,
    request: Request,
    admin_user_repo: AdminUserManagementDep
):
    """Deactivate traveller account"""
    try:
        admin_uc = AdminUserManagementUseCase(admin_user_repo)
        success = await admin_uc.deactivate_traveller(user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to deactivate traveller"
            )
        
        return UserActionResponse(
            success=True,
            message="Traveller deactivated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deactivating traveller: {str(e)}"
        )

@router.put("/hosts/{user_id}/remove-privileges", response_model=UserActionResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def remove_host_privileges(
    user_id: int,
    request: Request,
    admin_user_repo: AdminUserManagementDep
):
    """Remove host privileges from user"""
    try:
        admin_uc = AdminUserManagementUseCase(admin_user_repo)
        success = await admin_uc.remove_host_privileges(user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove host privileges"
            )
        
        return UserActionResponse(
            success=True,
            message="Host privileges removed successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing host privileges: {str(e)}"
        )

@router.put("/guides/{user_id}/remove-privileges", response_model=UserActionResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def remove_guide_privileges(
    user_id: int,
    request: Request,
    admin_user_repo: AdminUserManagementDep
):
    """Remove guide privileges from user"""
    try:
        admin_uc = AdminUserManagementUseCase(admin_user_repo)
        success = await admin_uc.remove_guide_privileges(user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove guide privileges"
            )
        
        return UserActionResponse(
            success=True,
            message="Guide privileges removed successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing guide privileges: {str(e)}"
        )


@router.put("/travellers/{user_id}/reactivate", response_model=UserActionResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def reactivate_traveller(
    user_id: int,
    request: Request,
    admin_user_repo: AdminUserManagementDep
):
    """Reactivate traveller account"""
    try:
        admin_uc = AdminUserManagementUseCase(admin_user_repo)
        success = await admin_uc.reactivate_traveller(user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to reactivate traveller"
            )
        
        return UserActionResponse(
            success=True,
            message="Traveller reactivated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reactivating traveller: {str(e)}"
        )

@router.put("/hosts/{user_id}/reinstate-privileges", response_model=UserActionResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def reinstate_host_privileges(
    user_id: int,
    request: Request,
    admin_user_repo: AdminUserManagementDep
):
    """Reinstate host privileges for user"""
    try:
        admin_uc = AdminUserManagementUseCase(admin_user_repo)
        success = await admin_uc.reinstate_host_privileges(user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to reinstate host privileges"
            )
        
        return UserActionResponse(
            success=True,
            message="Host privileges reinstated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reinstating host privileges: {str(e)}"
        )

@router.put("/guides/{user_id}/reinstate-privileges", response_model=UserActionResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def reinstate_guide_privileges(
    user_id: int,
    request: Request,
    admin_user_repo: AdminUserManagementDep
):
    """Reinstate guide privileges for user"""
    try:
        admin_uc = AdminUserManagementUseCase(admin_user_repo)
        success = await admin_uc.reinstate_guide_privileges(user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to reinstate guide privileges"
            )
        
        return UserActionResponse(
            success=True,
            message="Guide privileges reinstated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reinstating guide privileges: {str(e)}"
        )
