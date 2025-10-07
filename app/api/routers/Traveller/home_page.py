from fastapi import APIRouter, status, HTTPException, Depends
from starlette.requests import Request
from app.core.route_protection_validations.route_protection_dependencies import verify_traveller
from app.api.schemas.traveller.home_page import PropertySearchResultSchema, PropertySearchQueryParams
from app.core.entities.traveller.home_page import PropertySearchQueryEntity
from app.core.use_cases.traveller.home_page import TravellerHomePageUseCase
from app.api.dependencies import HomePageRepoDep
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/search', tags=['search'])


@router.get('/properties', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])
async def search_properties(
    request: Request,
    home_page_repo: HomePageRepoDep,
    query_params: PropertySearchQueryParams = Depends()
) -> PropertySearchResultSchema:
    """
    Search properties based on query parameters
    """
    try:
        # Create query entity from query params
        # Handle optional fields when all=True
        destination = query_params.destination or ""
        guests = query_params.guests or 1  # Default to 1 if not provided
        
        # Convert latitude and longitude to proper types
        latitude = None
        longitude = None
        if query_params.latitude is not None and query_params.latitude != "":
            try:
                latitude = float(query_params.latitude)
            except (ValueError, TypeError):
                latitude = None
        
        if query_params.longitude is not None and query_params.longitude != "":
            try:
                longitude = float(query_params.longitude)
            except (ValueError, TypeError):
                longitude = None
        
        query_entity = PropertySearchQueryEntity(
            destination=destination,
            guests=guests,
            from_date=query_params.fromDate,
            to_date=query_params.toDate,
            latitude=latitude,
            longitude=longitude,
            all=query_params.all,
            page=query_params.page,
            page_size=query_params.pageSize
        )
        
        # Initialize use case with injected repository
        use_case = TravellerHomePageUseCase(home_page_repo)
        
        # Validate query
        if not use_case.validate_search_query(query_entity):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid search parameters"
            )
        
        # Search properties
        result = await use_case.search_properties(query_entity)
        
        # Convert entities to response schema
        properties_response = []
        for prop in result.properties:
            property_response = {
                "id": prop.id,
                "propertyName": prop.property_name,
                "propertyDescription": prop.property_description,
                "maxGuests": prop.max_guests,
                "bedrooms": prop.bedrooms,
                "pricePerNight": prop.price_per_night,
                "propertyType": prop.property_type,
                "createdAt": prop.created_at,
                "updatedAt": prop.updated_at,
                "hostId": prop.host_id,
                "houseName": prop.house_name,
                "landmark": prop.landmark,
                "pincode": prop.pincode,
                "district": prop.district,
                "state": prop.state,
                "country": prop.country,
                "latitude": prop.latitude,
                "longitude": prop.longitude
            }
            properties_response.append(property_response)
        
        # Return response
        return PropertySearchResultSchema(
            properties=properties_response,
            totalCount=result.total_count,
            page=result.page,
            pageSize=result.page_size,
            message="Properties found successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in search_properties endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )