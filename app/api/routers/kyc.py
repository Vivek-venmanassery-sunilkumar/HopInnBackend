from fastapi import APIRouter, status, HTTPException, Depends, Query
from app.api.schemas import KycSchema, KycResponseSchema, KycAcceptRequestSchema, KycRejectRequestSchema
from starlette.requests import Request
from app.core.route_protection_validations.route_protection_dependencies import verify_traveller,verify_admin
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
        await kyc_uc.add_or_update_kyc(user_id=user_id, kyc_data=kyc_data)
        return "KYC details added successfully"
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'status': 'error', 'message': str(e)}
        ) 


@router.get('/get', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_traveller)], response_model=KycResponseSchema)
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
            detail={'status': 'error', 'message': str(e)}
        )

@router.get('/get-admin', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def get_kyc_admin(
        kyc_repo: KycRepoDep,
        status: str = Query(..., description="Filter by KYC status (required)"),
        page: int = Query(1, ge=1, description="Page number, default is 1"),
        limit: int = Query(10, ge=1, le=100, description="Items per page, default is 10, max is 100")
):
    kyc_uc = KycUseCase(kyc_repo=kyc_repo)
    return await kyc_uc.get_kyc_list(status= status, page=page, limit=limit)


@router.put('/accept-kyc', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def accept_kyc(
        kyc_repo: KycRepoDep,
        data: KycAcceptRequestSchema
):
    kyc_uc = KycUseCase(kyc_repo = kyc_repo)
    try:
        result = await kyc_uc.accept_kyc(user_id = data.userId)
        return {"success": result, "message": "Kyc accepted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail={'status': 'error', 'message':str(e)})


@router.put('/reject-kyc', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_admin)])
async def reject_kyc(
        kyc_repo: KycRepoDep,
        data: KycRejectRequestSchema
):
    kyc_uc = KycUseCase(kyc_repo = kyc_repo)
    try:
        result = await kyc_uc.reject_kyc(user_id = data.userId, rejection_reason = data.rejectionReason)
        return {"success": result, "message": "KYC rejected successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail={'status': 'error', 'message': str(e)})