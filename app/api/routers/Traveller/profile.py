from fastapi import APIRouter, status, HTTPException
from starlette.requests import Request
from app.api.dependencies import TravellerProfileDep
from app.core.use_cases import ProfileUseCase
from app.core.route_protection_validations.route_protection_decorators import requires_traveller

router = APIRouter(prefix='/profile',tags=['profile'])


@router.get('/detail', status_code=status.HTTP_200_OK)
@requires_traveller
async def get_profile_details(
    request: Request,
    traveller_profile: TravellerProfileDep
    ):
    profile_uc = ProfileUseCase(traveller_profile=traveller_profile)
    try:
        profile_details = profile_uc.get_profile_details(request.state.user_id)
        return profile_details
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )



