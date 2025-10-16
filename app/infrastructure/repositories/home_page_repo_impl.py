from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, or_, func
from sqlalchemy.future import select
from geoalchemy2 import functions as geo_funcs
from app.core.entities.traveller.home_page import PropertySearchEntity, PropertySearchQueryEntity, GuideSearchEntity, GuideSearchQueryEntity
from app.core.repositories.traveller_home_page import TravellerHomePageRepositoryInterface
from app.infrastructure.database.models.onboard import Property, PropertyAddress, PropertyImages, Guide, Languages
from app.infrastructure.database.models.users.user import User
import logging

logger = logging.getLogger(__name__)


class HomePageRepositoryImpl(TravellerHomePageRepositoryInterface):
    """Implementation of traveller home page repository"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def search_properties(
        self, 
        query: PropertySearchQueryEntity
    ) -> List[PropertySearchEntity]:
        """
        Search properties based on query parameters with geographic sorting and child-friendly prioritization
        """
        try:
            logger.info(f"Starting property search with query: all={query.all}, children_onboard={query.children_onboard}")
            
            # Build base query with primary image and distance calculation
            base_query = select(
                Property.id,
                Property.property_name,
                Property.property_description,
                Property.child_friendly,
                Property.max_guests,
                Property.bedrooms,
                Property.price_per_night,
                Property.property_type,
                Property.created_at,
                Property.updated_at,
                Property.host_id,
                PropertyAddress.house_name,
                PropertyAddress.landmark,
                PropertyAddress.pincode,
                PropertyAddress.district,
                PropertyAddress.state,
                PropertyAddress.country,
                func.ST_AsText(PropertyAddress.location).label('location_wkt'),
                PropertyImages.image_url.label('primary_image_url')
            ).join(
                PropertyAddress, Property.id == PropertyAddress.property_id
            ).outerjoin(
                PropertyImages, and_(
                    Property.id == PropertyImages.property_id,
                    PropertyImages.is_primary == True
                )
            )
            
            # Apply filters and sorting
            if not query.all:
                filters = []
                
                # Filter by guest capacity (only if guests is provided)
                if query.guests is not None:
                    filters.append(Property.max_guests >= query.guests)
                
                # Apply geographic search if coordinates are provided
                if query.latitude is not None and query.longitude is not None:
                    # Convert coordinates to geography point
                    search_point = self.convert_lat_lng_to_geography(query.latitude, query.longitude)
                    
                    # Add distance calculation for sorting using proper column reference
                    distance_calc = func.ST_Distance(
                        PropertyAddress.location,
                        func.ST_GeogFromText(search_point)
                    )
                    base_query = base_query.add_columns(distance_calc.label('distance'))
                    
                    # Add distance-based search (within 100km radius for better coverage)
                    distance_filter = func.ST_DWithin(
                        PropertyAddress.location,
                        func.ST_GeogFromText(search_point),
                        100000
                    )
                    filters.append(distance_filter)
                else:
                    # If no coordinates, add a default distance of 0 for sorting
                    base_query = base_query.add_columns(func.cast(0, func.Float).label('distance'))
                
                # Apply all filters
                if filters:
                    base_query = base_query.filter(and_(*filters))
                
                # Apply sorting based on children_onboard and geographic proximity
                if query.children_onboard is True:
                    # When children are onboard, prioritize child-friendly properties
                    # Sort by: child_friendly DESC, then by distance ASC
                    if query.latitude is not None and query.longitude is not None:
                        base_query = base_query.order_by(
                            Property.child_friendly.desc(),
                            distance_calc.asc()
                        )
                    else:
                        base_query = base_query.order_by(
                            Property.child_friendly.desc(),
                            Property.created_at.desc()
                        )
                else:
                    # When no children, sort primarily by distance
                    # Sort by: distance ASC, then by child_friendly DESC
                    if query.latitude is not None and query.longitude is not None:
                        base_query = base_query.order_by(
                            distance_calc.asc(),
                            Property.child_friendly.desc()
                        )
                    else:
                        base_query = base_query.order_by(
                            Property.child_friendly.desc(),
                            Property.created_at.desc()
                        )
            else:
                # For 'all' query, just sort by child_friendly and created_at
                logger.info("Processing 'all' query - no filters applied")
                base_query = base_query.order_by(
                    Property.child_friendly.desc(),
                    Property.created_at.desc()
                )
            
            # Add pagination
            offset = (query.page - 1) * query.page_size
            paginated_query = base_query.offset(offset).limit(query.page_size)
            logger.info(f"Executing query with pagination: offset={offset}, limit={query.page_size}")
            db_result = await self.db.execute(paginated_query)
            properties = db_result.all()
            logger.info(f"Query executed successfully, found {len(properties)} properties")
            
            # Convert to entities
            result = []
            for prop in properties:
                # Extract coordinates from WKT string
                coordinates = self._extract_coordinates_from_wkt(prop.location_wkt)
                
                entity = PropertySearchEntity(
                    id=prop.id,
                    property_name=prop.property_name,
                    property_description=prop.property_description,
                    child_friendly=prop.child_friendly,
                    max_guests=prop.max_guests,
                    bedrooms=prop.bedrooms,
                    price_per_night=prop.price_per_night,
                    property_type=prop.property_type,
                    created_at=prop.created_at,
                    updated_at=prop.updated_at,
                    host_id=prop.host_id,
                    house_name=prop.house_name,
                    landmark=prop.landmark,
                    pincode=prop.pincode,
                    district=prop.district,
                    state=prop.state,
                    country=prop.country,
                    latitude=coordinates.get('latitude'),
                    longitude=coordinates.get('longitude'),
                    primary_image_url=prop.primary_image_url
                )
                result.append(entity)
            
            logger.info(f"Found {len(result)} properties matching search criteria")
            return result
            
        except Exception as e:
            logger.error(f"Error searching properties: {str(e)}")
            raise

    async def get_properties_count(
        self, 
        query: PropertySearchQueryEntity
    ) -> int:
        """
        Get total count of properties matching search criteria
        """
        try:
            # Build base query
            base_query = select(Property.id).join(
                PropertyAddress, Property.id == PropertyAddress.property_id
            ).outerjoin(
                PropertyImages, and_(
                    Property.id == PropertyImages.property_id,
                    PropertyImages.is_primary == True
                )
            )
            
            # Apply filters (same logic as search_properties but without sorting)
            if not query.all:
                filters = []
                
                # Filter by guest capacity (only if guests is provided)
                if query.guests is not None:
                    filters.append(Property.max_guests >= query.guests)
                
                # Apply geographic search if coordinates are provided
                if query.latitude is not None and query.longitude is not None:
                    # Convert coordinates to geography point
                    search_point = self.convert_lat_lng_to_geography(query.latitude, query.longitude)
                    
                    # Add distance-based search (within 100km radius for better coverage)
                    distance_filter = func.ST_DWithin(
                        PropertyAddress.location,
                        func.ST_GeogFromText(search_point),
                        100000
                    )
                    filters.append(distance_filter)
                
                # Apply all filters and count
                if filters:
                    base_query = base_query.filter(and_(*filters))
            
            # Execute count query
            count_result = await self.db.execute(select(func.count()).select_from(base_query.subquery()))
            count = count_result.scalar()
            logger.info(f"Total properties matching search criteria: {count}")
            return count
            
        except Exception as e:
            logger.error(f"Error getting properties count: {str(e)}")
            raise

    def convert_lat_lng_to_geography(self, latitude: float, longitude: float) -> str:
        """
        Convert latitude and longitude to PostGIS geography point
        """
        return f"POINT({longitude} {latitude})"

    def parse_destination_hierarchy(self, destination: str) -> dict:
        """
        Parse destination string to extract location hierarchy
        """
        try:
            # Split destination by comma and clean up
            parts = [part.strip() for part in destination.split(',')]
            
            hierarchy = {
                'city': None,
                'district': None,
                'state': None,
                'country': None
            }
            
            # Mapbox typically returns: "City, District, State, Country"
            if len(parts) >= 1:
                hierarchy['city'] = parts[0]
            if len(parts) >= 2:
                hierarchy['district'] = parts[1]
            if len(parts) >= 3:
                hierarchy['state'] = parts[2]
            if len(parts) >= 4:
                hierarchy['country'] = parts[3]
            
            logger.info(f"Parsed destination hierarchy: {hierarchy}")
            return hierarchy
            
        except Exception as e:
            logger.error(f"Error parsing destination hierarchy: {str(e)}")
            return {'city': None, 'district': None, 'state': None, 'country': None}

    def _extract_coordinates_from_wkt(self, wkt_string: str) -> dict:
        """
        Extract coordinates from WKT string
        """
        coordinates = {'latitude': None, 'longitude': None}
        
        if wkt_string and wkt_string.startswith('POINT('):
            try:
                # Remove 'POINT(' and ')' and split coordinates
                coords_str = wkt_string[6:-1]
                coords = coords_str.split()
                if len(coords) == 2:
                    coordinates = {
                        'longitude': float(coords[0]),
                        'latitude': float(coords[1])
                    }
            except (ValueError, IndexError) as e:
                logger.warning(f"Error parsing WKT coordinates: {e}")
        
        return coordinates

    async def search_guides(
        self, 
        query: GuideSearchQueryEntity
    ) -> List[GuideSearchEntity]:
        """
        Search guides based on query parameters with geographic sorting
        """
        try:
            logger.info(f"Starting guide search with query: all={query.all}, destination={query.destination}")
            
            # Build base query with user details and languages
            base_query = select(
                Guide.id,
                Guide.user_id,
                Guide.bio,
                Guide.profession,
                Guide.expertise,
                Guide.hourly_rate,
                Guide.house_name,
                Guide.landmark,
                Guide.pincode,
                Guide.district,
                Guide.state,
                Guide.country,
                func.ST_AsText(Guide.location).label('location_wkt'),
                Guide.created_at,
                Guide.updated_at,
                User.first_name,
                User.last_name,
                User.profile_image
            ).join(
                User, Guide.user_id == User.id
            ).where(
                Guide.is_blocked == False  # Only get non-blocked guides
            )
            
            # Apply filters and sorting
            if not query.all:
                filters = []
                
                logger.info(f"Applying guide filters - destination: '{query.destination}', coordinates: ({query.latitude}, {query.longitude})")
                
                # Parse destination to extract location hierarchy (only if destination is provided)
                if query.destination:
                    location_hierarchy = self.parse_destination_hierarchy(query.destination)
                    logger.info(f"Parsed destination hierarchy: {location_hierarchy}")
                    
                    # Create OR conditions for multiple location fields to increase match chances
                    location_filters = []
                    
                    # Search by city (district field often contains city names)
                    if location_hierarchy.get('city'):
                        location_filters.append(Guide.district.ilike(f"%{location_hierarchy['city']}%"))
                        logger.info(f"Added city filter (district): {location_hierarchy['city']}")
                    
                    # Search by district
                    if location_hierarchy.get('district'):
                        location_filters.append(Guide.district.ilike(f"%{location_hierarchy['district']}%"))
                        logger.info(f"Added district filter: {location_hierarchy['district']}")
                    
                    # Search by state
                    if location_hierarchy.get('state'):
                        location_filters.append(Guide.state.ilike(f"%{location_hierarchy['state']}%"))
                        logger.info(f"Added state filter: {location_hierarchy['state']}")
                    
                    # Search by country
                    if location_hierarchy.get('country'):
                        location_filters.append(Guide.country.ilike(f"%{location_hierarchy['country']}%"))
                        logger.info(f"Added country filter: {location_hierarchy['country']}")
                    
                    # Add OR condition for any location match
                    if location_filters:
                        filters.append(or_(*location_filters))
                        logger.info(f"Added OR location filter with {len(location_filters)} conditions")
                
                # Apply geographic search if coordinates are provided
                if query.latitude is not None and query.longitude is not None:
                    # Convert coordinates to geography point
                    search_point = self.convert_lat_lng_to_geography(query.latitude, query.longitude)
                    logger.info(f"Search point: {search_point}")
                    
                    # Add distance calculation for sorting using proper column reference
                    distance_calc = func.ST_Distance(
                        Guide.location,
                        func.ST_GeogFromText(search_point)
                    )
                    base_query = base_query.add_columns(distance_calc.label('distance'))
                    
                    # Add distance-based search (within 100km radius for better coverage)
                    distance_filter = func.ST_DWithin(
                        Guide.location,
                        func.ST_GeogFromText(search_point),
                        100000
                    )
                    filters.append(distance_filter)
                    logger.info("Added geographic distance filter (100km radius)")
                else:
                    # If no coordinates, add a default distance of 0 for sorting
                    base_query = base_query.add_columns(func.cast(0, func.Float).label('distance'))
                
                # Apply all filters
                if filters:
                    base_query = base_query.filter(and_(*filters))
                    logger.info(f"Applied {len(filters)} filters to guide search")
                else:
                    logger.info("No filters applied to guide search")
                
                # Apply sorting based on geographic proximity
                if query.latitude is not None and query.longitude is not None:
                    # Sort by distance ASC (closest first)
                    base_query = base_query.order_by(distance_calc.asc())
                    logger.info("Applied distance-based sorting")
                else:
                    # If no coordinates, sort by created_at DESC
                    base_query = base_query.order_by(Guide.created_at.desc())
                    logger.info("Applied created_at sorting")
            else:
                # For 'all' query, just sort by created_at
                logger.info("Processing 'all' query for guides - no filters applied")
                base_query = base_query.order_by(Guide.created_at.desc())
            
            # Debug: Let's check what guides exist in the database
            debug_query = select(Guide.id, Guide.district, Guide.state, Guide.country, Guide.is_blocked).where(Guide.is_blocked == False)
            debug_result = await self.db.execute(debug_query)
            all_guides = debug_result.all()
            logger.info(f"Total guides in database (not blocked): {len(all_guides)}")
            for guide in all_guides:
                logger.info(f"Guide {guide.id}: district='{guide.district}', state='{guide.state}', country='{guide.country}'")
            
            # Add pagination
            offset = (query.page - 1) * query.page_size
            paginated_query = base_query.offset(offset).limit(query.page_size)
            logger.info(f"Executing guide query with pagination: offset={offset}, limit={query.page_size}")
            
            db_result = await self.db.execute(paginated_query)
            guides = db_result.all()
            logger.info(f"Query executed successfully, found {len(guides)} guides")
            
            # Convert to entities
            result = []
            for guide in guides:
                # Extract coordinates from WKT string
                coordinates = self._extract_coordinates_from_wkt(guide.location_wkt)
                
                # Get languages for this guide
                languages_query = select(Languages.language).where(Languages.user_id == guide.user_id)
                languages_result = await self.db.execute(languages_query)
                known_languages = [lang.language for lang in languages_result.all()]
                
                entity = GuideSearchEntity(
                    id=guide.id,
                    user_id=guide.user_id,
                    bio=guide.bio,
                    profession=guide.profession,
                    expertise=guide.expertise,
                    hourly_rate=guide.hourly_rate,
                    house_name=guide.house_name,
                    landmark=guide.landmark,
                    pincode=guide.pincode,
                    district=guide.district,
                    state=guide.state,
                    country=guide.country,
                    latitude=coordinates.get('latitude'),
                    longitude=coordinates.get('longitude'),
                    created_at=guide.created_at,
                    updated_at=guide.updated_at,
                    first_name=guide.first_name,
                    last_name=guide.last_name,
                    profile_image=guide.profile_image,
                    known_languages=known_languages
                )
                result.append(entity)
            
            logger.info(f"Found {len(result)} guides matching search criteria")
            return result
            
        except Exception as e:
            logger.error(f"Error searching guides: {str(e)}")
            raise

    async def get_guides_count(
        self, 
        query: GuideSearchQueryEntity
    ) -> int:
        """
        Get total count of guides matching search criteria
        """
        try:
            # Build base query with count
            base_query = select(func.count(Guide.id)).join(
                User, Guide.user_id == User.id
            ).where(
                Guide.is_blocked == False  # Only count non-blocked guides
            )
            
            # Apply filters only if not requesting all guides
            if not query.all:
                filters = []
                
                # Parse destination to extract location hierarchy (only if destination is provided)
                if query.destination:
                    location_hierarchy = self.parse_destination_hierarchy(query.destination)
                    
                    # Create OR conditions for multiple location fields to increase match chances
                    location_filters = []
                    
                    # Search by city (district field often contains city names)
                    if location_hierarchy.get('city'):
                        location_filters.append(Guide.district.ilike(f"%{location_hierarchy['city']}%"))
                    
                    # Search by district
                    if location_hierarchy.get('district'):
                        location_filters.append(Guide.district.ilike(f"%{location_hierarchy['district']}%"))
                    
                    # Search by state
                    if location_hierarchy.get('state'):
                        location_filters.append(Guide.state.ilike(f"%{location_hierarchy['state']}%"))
                    
                    # Search by country
                    if location_hierarchy.get('country'):
                        location_filters.append(Guide.country.ilike(f"%{location_hierarchy['country']}%"))
                    
                    # Add OR condition for any location match
                    if location_filters:
                        filters.append(or_(*location_filters))
                
                # Apply geographic search if coordinates are provided
                if query.latitude is not None and query.longitude is not None:
                    # Convert coordinates to geography point
                    search_point = self.convert_lat_lng_to_geography(query.latitude, query.longitude)
                    
                    # Add distance-based search (within 100km radius for better coverage)
                    distance_filter = func.ST_DWithin(
                        Guide.location,
                        func.ST_GeogFromText(search_point),
                        100000
                    )
                    filters.append(distance_filter)
                
                # Apply all filters and count
                if filters:
                    base_query = base_query.filter(and_(*filters))
            
            # Execute count query
            count_result = await self.db.execute(base_query)
            count = count_result.scalar()
            logger.info(f"Total guides matching search criteria: {count}")
            return count
            
        except Exception as e:
            logger.error(f"Error getting guides count: {str(e)}")
            raise
