from fastapi import APIRouter, status, HTTPException, Depends
from starlette.requests import Request
from app.core.route_protection_validations.route_protection_dependencies import verify_traveller
from app.api.schemas.traveller.home_page import PropertySearchResultSchema, PropertySearchQueryParams, GuideSearchResultSchema, GuideSearchQueryParams, GuideSearchResponseSchema
from app.core.entities.traveller.home_page import PropertySearchQueryEntity, GuideSearchQueryEntity
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
            children_onboard=query_params.childrenOnboard,
            all=query_params.all,
            page=query_params.page,
            page_size=query_params.pageSize
        )
        
        # Initialize use case with injected repository
        use_case = TravellerHomePageUseCase(home_page_repo)
        
        # Search properties (validation is handled in schema layer)
        result = await use_case.search_properties(query_entity)
        
        # Convert entities to response schema
        properties_response = []
        for prop in result.properties:
            property_response = {
                "id": prop.id,
                "propertyName": prop.property_name,
                "propertyDescription": prop.property_description,
                "childFriendly": prop.child_friendly,
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
                "longitude": prop.longitude,
                "primaryImageUrl": prop.primary_image_url
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


@router.get('/guides', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])
async def search_guides(
    request: Request,
    home_page_repo: HomePageRepoDep,
    query_params: GuideSearchQueryParams = Depends()
) -> GuideSearchResultSchema:
    """
    Search guides based on query parameters
    """
    try:
        # Create query entity from query params
        # Handle optional fields when all=True
        destination = query_params.destination or ""
        
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
        
        query_entity = GuideSearchQueryEntity(
            destination=destination,
            latitude=latitude,
            longitude=longitude,
            children_onboard=query_params.childrenOnboard,
            all=query_params.all,
            page=query_params.page,
            page_size=query_params.pageSize
        )
        
        # Initialize use case with injected repository
        use_case = TravellerHomePageUseCase(home_page_repo)
        
        # Search guides (validation is handled in schema layer)
        result = await use_case.search_guides(query_entity)
        
        # Convert entities to response schema
        guides_response = []
        for guide in result.guides:
            guide_response = {
                "id": guide.id,
                "userId": guide.user_id,
                "bio": guide.bio,
                "profession": guide.profession,
                "expertise": guide.expertise,
                "hourlyRate": guide.hourly_rate,
                "houseName": guide.house_name,
                "landmark": guide.landmark,
                "pincode": guide.pincode,
                "district": guide.district,
                "state": guide.state,
                "country": guide.country,
                "latitude": guide.latitude,
                "longitude": guide.longitude,
                "createdAt": guide.created_at,
                "updatedAt": guide.updated_at,
                "firstName": guide.first_name,
                "lastName": guide.last_name,
                "profileImage": guide.profile_image,
                "knownLanguages": guide.known_languages
            }
            guides_response.append(guide_response)
        
        # Return response
        return GuideSearchResultSchema(
            guides=guides_response,
            totalCount=result.total_count,
            page=result.page,
            pageSize=result.page_size,
            message="Guides found successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in search_guides endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get('/guide/{guide_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])
async def get_guide_details(
    guide_id: int,
    request: Request,
    home_page_repo: HomePageRepoDep
) -> GuideSearchResponseSchema:
    """
    Get guide details by ID
    """
    try:
        # Create a query to get the specific guide
        query_entity = GuideSearchQueryEntity(
            destination="",
            latitude=None,
            longitude=None,
            all=True,  # Get all guides and filter by ID in the repository
            page=1,
            page_size=1
        )
        
        # Initialize use case with injected repository
        use_case = TravellerHomePageUseCase(home_page_repo)
        
        # Get all guides and find the specific one
        result = await use_case.search_guides(query_entity)
        
        # Find the guide with the matching ID
        guide = None
        for g in result.guides:
            if g.id == guide_id:
                guide = g
                break
        
        if not guide:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Guide not found"
            )
        
        # Convert entity to response schema
        guide_response = {
            "id": guide.id,
            "userId": guide.user_id,
            "bio": guide.bio,
            "profession": guide.profession,
            "expertise": guide.expertise,
            "hourlyRate": guide.hourly_rate,
            "houseName": guide.house_name,
            "landmark": guide.landmark,
            "pincode": guide.pincode,
            "district": guide.district,
            "state": guide.state,
            "country": guide.country,
            "latitude": guide.latitude,
            "longitude": guide.longitude,
            "createdAt": guide.created_at,
            "updatedAt": guide.updated_at,
            "firstName": guide.first_name,
            "lastName": guide.last_name,
            "profileImage": guide.profile_image,
            "knownLanguages": guide.known_languages
        }
        
        return GuideSearchResponseSchema(**guide_response)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_guide_details endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )