from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, and_, or_, func
from sqlalchemy.future import select
from geoalchemy2 import functions as geo_funcs
from app.core.entities.traveller.home_page import PropertySearchEntity, PropertySearchQueryEntity
from app.core.repositories.traveller_home_page import TravellerHomePageRepositoryInterface
from app.infrastructure.database.models.onboard import Property, PropertyAddress
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
        Search properties based on query parameters
        """
        try:
            # Build base query
            base_query = select(
                Property.id,
                Property.property_name,
                Property.property_description,
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
                func.ST_AsText(PropertyAddress.location).label('location_wkt')
            ).join(
                PropertyAddress, Property.id == PropertyAddress.property_id
            )
            
            # Apply filters only if not requesting all properties
            if not query.all:
                filters = []
                
                # Parse destination to extract location hierarchy (only if destination is provided)
                if query.destination:
                    location_hierarchy = self.parse_destination_hierarchy(query.destination)
                    
                    # Filter by location hierarchy if available
                    if location_hierarchy.get('district'):
                        filters.append(PropertyAddress.district.ilike(f"%{location_hierarchy['district']}%"))
                    elif location_hierarchy.get('state'):
                        filters.append(PropertyAddress.state.ilike(f"%{location_hierarchy['state']}%"))
                    elif location_hierarchy.get('country'):
                        filters.append(PropertyAddress.country.ilike(f"%{location_hierarchy['country']}%"))
                
                # Filter by guest capacity (only if guests is provided)
                if query.guests is not None:
                    filters.append(Property.max_guests >= query.guests)
                
                # Apply geographic search if coordinates are provided
                if query.latitude is not None and query.longitude is not None:
                    # Convert coordinates to geography point
                    search_point = self.convert_lat_lng_to_geography(query.latitude, query.longitude)
                    
                    # Add distance-based search (within 50km radius)
                    distance_filter = text(
                        f"ST_DWithin(property_address.location, ST_GeogFromText('{search_point}'), 50000)"
                    )
                    filters.append(distance_filter)
                
                # Apply all filters
                if filters:
                    base_query = base_query.filter(and_(*filters))
            
            # Add pagination
            offset = (query.page - 1) * query.page_size
            paginated_query = base_query.offset(offset).limit(query.page_size)
            db_result = await self.db.execute(paginated_query)
            properties = db_result.all()
            
            # Convert to entities
            result = []
            for prop in properties:
                # Extract coordinates from WKT string
                coordinates = self._extract_coordinates_from_wkt(prop.location_wkt)
                
                entity = PropertySearchEntity(
                    id=prop.id,
                    property_name=prop.property_name,
                    property_description=prop.property_description,
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
                    longitude=coordinates.get('longitude')
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
            )
            
            # Apply filters only if not requesting all properties
            if not query.all:
                filters = []
                
                # Parse destination to extract location hierarchy (only if destination is provided)
                if query.destination:
                    location_hierarchy = self.parse_destination_hierarchy(query.destination)
                    
                    # Filter by location hierarchy if available
                    if location_hierarchy.get('district'):
                        filters.append(PropertyAddress.district.ilike(f"%{location_hierarchy['district']}%"))
                    elif location_hierarchy.get('state'):
                        filters.append(PropertyAddress.state.ilike(f"%{location_hierarchy['state']}%"))
                    elif location_hierarchy.get('country'):
                        filters.append(PropertyAddress.country.ilike(f"%{location_hierarchy['country']}%"))
                
                # Filter by guest capacity (only if guests is provided)
                if query.guests is not None:
                    filters.append(Property.max_guests >= query.guests)
                
                # Apply geographic search if coordinates are provided
                if query.latitude is not None and query.longitude is not None:
                    # Convert coordinates to geography point
                    search_point = self.convert_lat_lng_to_geography(query.latitude, query.longitude)
                    
                    # Add distance-based search (within 50km radius)
                    distance_filter = text(
                        f"ST_DWithin(property_address.location, ST_GeogFromText('{search_point}'), 50000)"
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
