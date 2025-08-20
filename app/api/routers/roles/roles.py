from fastapi import APIRouter, status, Request
from app.api.dependencies import UserRepoDep


router = APIRouter(prefix='/roles', tags=['roles'])

@router.get('/', status_code=status.HTTP_200_OK)
async def get_roles(
    request: Request,
    user_repo: UserRepoDep
    ):
    user_id = request.state.user_id
    user_roles = await user_repo.get_user_roles(user_id)
    if not user_roles:
        raise ValueError('The user id is not found')
    
    return user_roles
    

    
