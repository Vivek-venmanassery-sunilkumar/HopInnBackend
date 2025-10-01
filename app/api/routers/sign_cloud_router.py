from fastapi import APIRouter, status, HTTPException
from app.core.use_cases import CloudinaryUseCase 


router = APIRouter(prefix='/cloudinary',tags=['sign-cloud'])


@router.get('/signature', status_code=status.HTTP_200_OK)
async def sign_cloud_upload():
    signed_params = CloudinaryUseCase.generate_upload_signature()
    return signed_params

@router.delete('/image/{public_id}', status_code=status.HTTP_200_OK)
async def delete_cloudinary_image(public_id: str):
    try:
        success = CloudinaryUseCase.delete_image(public_id)
        if success:
            return {'success': True, 'message': 'Image deleted successfully'}
        else:
            raise HTTPException(status_code=400, detail='Failed to delete image')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error deleting image: {str(e)}')
    