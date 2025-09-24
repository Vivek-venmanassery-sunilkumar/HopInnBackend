from fastapi import APIRouter, status, HTTPException, Depends
from starlette.requests import Request
from app.core.route_protection_validations.route_protection_dependencies import verify_guide
from app.api.dependencies import GuideProfileDep
from app.core.use_cases import GuideProfileUseCase

router = APIRouter(prefix='/guide-profile',tags=['guide-profile'])


@router.get('/detail', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_guide)])
async def get_guide_profile(
    request: Request,
    guide_profile_repo: GuideProfileDep
):
    guide_profile_uc = GuideProfileUseCase(guide_profile_repo)

    try:
        guide_profile = await guide_profile_uc.get_profile_details(user_id = request.state.user_id)
        return guide_profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

