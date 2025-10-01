from fastapi import APIRouter, status, Depends
from starlette.requests import Request
from app.api.schemas import PropertySchema
from app.api.dependencies import PropertyRepoDepo
from app.core.use_cases import PropertyUseCase
from app.core.route_protection_validations.route_protection_dependencies import verify_host


router = APIRouter(prefix='/property', tags=['property-management'])

@router.post('/add', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_host)])
async def add_property(
    request: Request,
    property_data: PropertySchema,
    property_repo: PropertyRepoDepo
):
    property_uc = PropertyUseCase(property_repo = property_repo)
    property_id = await property_uc.add_property(user_id=request.state.user_id, property_data=property_data)
    if property_id:
        return {'success': True, 'message': 'Property added successfully'}
    return {'success': False, 'message': 'Property adding failed'}

@router.get('/get', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_host)])
async def get_properties(
    request: Request,
    property_repo: PropertyRepoDepo
):
    property_uc = PropertyUseCase(property_repo=property_repo)
    properties = await property_uc.get_property(request.state.user_id)
    properties_data = [prop.model_dump(by_alias=True) for prop in properties]
    return {
        "success": True,
        "data": properties_data,
        "message": "Properties fetched successfully"
    }

@router.put('/edit', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_host)])
async def edit_properties(
    request: Request,
):
    pass
