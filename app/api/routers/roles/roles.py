from fastapi import APIRouter, status, Request
from app.api.dependencies import UserRepoDep, KycRepoDep


router = APIRouter(prefix='/roles', tags=['roles'])

#Route to identify roles/permissions for the frontend - UserRoles schema is returned(formatted for frontend)
@router.get('/', status_code=status.HTTP_200_OK)
async def get_roles(
    request: Request,
    user_repo: UserRepoDep,
    kyc_repo: KycRepoDep
    ):
    user_id = request.state.user_id
    user_roles = await user_repo.get_user_roles(user_id)
    if not user_roles:
        raise ValueError('The user id is not found')

    kyc_verified = await kyc_repo.check_kyc_accepted(user_id)
    user_roles.isKycVerified = kyc_verified
    
    return user_roles
    

    
