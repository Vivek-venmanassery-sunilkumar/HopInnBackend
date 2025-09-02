from fastapi import APIRouter, status, HTTPException, Depends
from app.api.schemas import KycSchema
from starlette.requests import Request
from app.core.route_protection_validations.route_protection_dependencies import verify_traveller
from app.api.dependencies import KycRepoDep
from app.core.use_cases import KycUseCase


router = APIRouter(prefix='/kyc', tags=['kyc'])


@router.post('/add', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])
async def update_kyc_details(
    request: Request,
    kyc_data: KycSchema,
    kyc_repo: KycRepoDep,
):
    user_id = request.state.user_id
    kyc_uc = KycUseCase(kyc_repo=kyc_repo)
    try:
        await kyc_uc.add_kyc(user_id=user_id, kyc_data=kyc_data)
        return "KYC details added successfully"
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 


@router.get('/get', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])
async def get_kyc_details(
    request: Request,
    kyc_repo: KycRepoDep,
):
    user_id = request.state.user_id
    kyc_uc = KycUseCase(kyc_repo=kyc_repo)
    try:
        kyc_details = await kyc_uc.get_kyc(user_id=user_id)
        if not kyc_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="KYC details not found"
            )
        return kyc_details
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )