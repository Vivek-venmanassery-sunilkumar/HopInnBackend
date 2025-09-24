from fastapi import APIRouter, status, HTTPException, Depends
from starlette.requests import Request
from app.core.route_protection_validations.route_protection_dependencies import verify_host
from app.api.dependencies import HostProfileDep
from app.core.use_cases import HostProfileUseCase

router = APIRouter(prefix='/host-profile', tags=['host-profile'])

@router.get('/detail', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_host)])
async def get_host_profile(
    request: Request,
    host_profile_repo: HostProfileDep
):
    host_profile_uc = HostProfileUseCase(host_profile_repo)

    try:
        host_profile = await host_profile_uc.get_profile_details(user_id = request.state.user_id)
        return host_profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )