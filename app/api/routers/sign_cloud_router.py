from fastapi import APIRouter, status
from app.core.use_cases import CloudinaryUseCase 


router = APIRouter(prefix='/cloudinary',tags=['sign-cloud'])


@router.get('/signature', status_code=status.HTTP_200_OK)
async def sign_cloud_upload():
    signed_params = CloudinaryUseCase.generate_upload_signature()
    return signed_params
    