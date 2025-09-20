from fastapi import APIRouter, status, HTTPException, Depends
from starlette.requests import Request
from app.api.dependencies import TravellerProfileDep
from app.core.use_cases import TravellerProfileUseCase, CloudinaryUseCase
from app.core.route_protection_validations.route_protection_dependencies import verify_traveller
from app.api.schemas import TravellerProfileUpdateSchema

router = APIRouter(prefix='/profile',tags=['profile'])


@router.get('/detail', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])
async def get_profile_details(
    request: Request,
    traveller_profile: TravellerProfileDep
    ):
    profile_uc = TravellerProfileUseCase(traveller_profile=traveller_profile)
    try:
        profile_details = await profile_uc.get_profile_details(user_id = request.state.user_id)
        return profile_details
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put('/update', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])
async def update_profile_detials(
    request: Request,
    update_data: TravellerProfileUpdateSchema,
    traveller_profile: TravellerProfileDep
):
    profile_uc = TravellerProfileUseCase(traveller_profile=traveller_profile)
    try: 
        if update_data.profileImageUrl:
            public_id = await profile_uc.get_public_id(user_id = request.state.user_id)
            if public_id:
                CloudinaryUseCase.delete_image(public_id)
        await profile_uc.update_profile_details(user_id = request.state.user_id, update_details=update_data)
        del update_data.profileImagePublicId
        return update_data
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= str(e)
        )

