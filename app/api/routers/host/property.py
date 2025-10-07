from fastapi import APIRouter, status, Depends, HTTPException
from starlette.requests import Request
from app.api.schemas import PropertySchema, PropertyUpdateSchema, PropertyDetailsResponseSchema
from app.api.dependencies import PropertyRepoDepo
from app.core.use_cases import PropertyUseCase
from app.core.route_protection_validations.route_protection_dependencies import verify_host, verify_traveller


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
    property_data: PropertyUpdateSchema,
    property_repo: PropertyRepoDepo
):
    try:
        property_uc = PropertyUseCase(property_repo=property_repo)
        success = await property_uc.update_property(
            user_id=request.state.user_id, 
            property_data=property_data
        )
        
        if success:
            return {
                'success': True, 
                'message': 'Property updated successfully'
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Failed to update property. Property may not exist or you may not have permission to update it.'
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error updating property: {str(e)}'
        )

@router.get('/get_by_id/{property_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])
async def get_property_by_id(
    property_id: int,
    property_repo: PropertyRepoDepo
) -> PropertyDetailsResponseSchema:
    """
    Get property details by ID for travellers
    """
    try:
        property_uc = PropertyUseCase(property_repo=property_repo)
        property_data = await property_uc.get_property_details_by_id(property_id)
        
        if not property_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )
        
        # Convert entity to response schema
        property_dict = property_data.model_dump(by_alias=True)
        
        return PropertyDetailsResponseSchema(**property_dict)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error fetching property: {str(e)}'
        )
