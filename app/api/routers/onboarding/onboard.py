from fastapi import APIRouter, status, HTTPException, Depends
from app.api.schemas import GuideOnboardSchema, HostOnboardSchema
from app.api.dependencies import KycRepoDep, OnboardRepoDep
from app.core.use_cases import OnBoardingUseCase
from app.core.entities import GuideOnboardEntity, HostOnboardEntity, PropertyAddressEntity, PropertyImageEntity
from starlette.requests import Request
from app.core.exceptions import KycNotAcceptedError
from app.core.route_protection_validations.route_protection_dependencies import verify_traveller
import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix='/onboard', tags=['onboarding_roles'])


@router.post('/guide', status_code = status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])
async def onboard_guide(
    request: Request,
    guide_data: GuideOnboardSchema,
    onboarding_repo: OnboardRepoDep,
    kyc_repo: KycRepoDep,
):
    onboard_uc = OnBoardingUseCase(
      kyc_repo=kyc_repo,
      onboard_repo=onboarding_repo
   )

    try:
        result = await onboard_uc.onboard_guide(
            data=GuideOnboardEntity(**guide_data.model_dump()),
            user_id= request.state.user_id
        )

        return {"success": True, "message": "Guide onboarded successfully"}
    except KycNotAcceptedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="KYC must be approved before becoming a guide"
        )
    except Exception as e:
        logger.info(str(e)) 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post('/host', status_code = status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])    
async def onboard_host(
        request: Request,
        host_data:HostOnboardSchema,
        onboarding_repo: OnboardRepoDep,
        kyc_repo: KycRepoDep
):
    onboard_uc = OnBoardingUseCase(
       kyc_repo=kyc_repo,
       onboard_repo=onboarding_repo
    )

    try:
        host_entity = HostOnboardEntity(
            **host_data.model_dump()
        ) 

        result = await onboard_uc.onboard_host(
            user_id=request.state.user_id,
            data = host_entity
        )
        return {"success": True, "message": "Host onboarded successfully"}
    except KycNotAcceptedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="KYC must be approved before becoming a host"
        )
    except Exception as e:
        logger.info(str(e)) 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 

