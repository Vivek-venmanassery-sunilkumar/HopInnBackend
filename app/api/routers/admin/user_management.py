from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Union
from app.core.use_cases.admin.user_management_use_case import UserManagementUseCase
from app.api.schemas import TravellerUserSchema, GuideUserSchema, HostUserSchema, UserStatusUpdateRequestSchema, UserStatusUpdateResponseSchema
from app.core.route_protection_validations.route_protection_dependencies import verify_admin
from app.api.dependencies import UserManagementRepoDep

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=List[Union[TravellerUserSchema, GuideUserSchema, HostUserSchema]], dependencies=[Depends(verify_admin)])
async def get_users_by_role(
    user_management_repo: UserManagementRepoDep,
    role: str = Query(..., description="User role: traveller, guide, or host"),
):
    """
    Get users by role (traveller, guide, or host)
    """
    if role not in ["traveller", "guide", "host"]:
        raise HTTPException(
            status_code=400, 
            detail="Invalid role. Role must be 'traveller', 'guide', or 'host'"
        )
    
    try:
        user_management_use_case = UserManagementUseCase(user_management_repo)
        users = await user_management_use_case.get_users_by_role(role)
        return users
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/users/traveller/status", response_model=UserStatusUpdateResponseSchema, dependencies=[Depends(verify_admin)])
async def update_traveller_status(
    user_management_repo: UserManagementRepoDep,
    request: UserStatusUpdateRequestSchema
):
    """
    Update traveller status (is_active in User model)
    If blocking traveller, also block their guide and host privileges
    """
    try:
        user_management_use_case = UserManagementUseCase(user_management_repo)
        result = await user_management_use_case.update_traveller_status(
            email=request.email,
            is_active=request.is_active
        )
        return UserStatusUpdateResponseSchema(message="Traveller status updated successfully", data=result)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/users/guide/status", response_model=UserStatusUpdateResponseSchema, dependencies=[Depends(verify_admin)])
async def update_guide_status(
    user_management_repo: UserManagementRepoDep,
    request: UserStatusUpdateRequestSchema
):
    """
    Update guide status (is_blocked in Guide model)
    """
    try:
        user_management_use_case = UserManagementUseCase(user_management_repo)
        result = await user_management_use_case.update_guide_status(
            email=request.email,
            is_blocked=request.is_blocked
        )
        return UserStatusUpdateResponseSchema(message="Guide status updated successfully", data=result)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/users/host/status", response_model=UserStatusUpdateResponseSchema, dependencies=[Depends(verify_admin)])
async def update_host_status(
    user_management_repo: UserManagementRepoDep,
    request: UserStatusUpdateRequestSchema
):
    """
    Update host status (is_blocked in Host model)
    """
    try:
        user_management_use_case = UserManagementUseCase(user_management_repo)
        result = await user_management_use_case.update_host_status(
            email=request.email,
            is_blocked=request.is_blocked
        )
        return UserStatusUpdateResponseSchema(message="Host status updated successfully", data=result)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
