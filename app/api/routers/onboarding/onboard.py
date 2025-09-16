from fastapi import APIRouter, status, HTTPException
from app.api.schemas import GuideOnboardSchema
from app.api.dependencies import KycRepoDep, OnboardRepoDep
from app.core.use_cases import OnBoardingUseCase
from app.core.entities import GuideOnboardEntity
from starlette.requests import Request
from app.core.exceptions import KycNotAcceptedError
import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix='/onboard', tags=['onboarding_roles'])


@router.post('/guide', status_code = status.HTTP_200_OK)
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
    
