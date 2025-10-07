from typing import List
from app.core.entities.traveller.home_page import PropertySearchEntity, PropertySearchQueryEntity, PropertySearchResultEntity
from app.core.repositories.traveller_home_page import TravellerHomePageRepositoryInterface
import logging

logger = logging.getLogger(__name__)


class TravellerHomePageUseCase:
    """Use case for traveller home page operations"""

    def __init__(self, repository: TravellerHomePageRepositoryInterface):
        self.repository = repository

    async def search_properties(
        self, 
        query: PropertySearchQueryEntity
    ) -> PropertySearchResultEntity:
        """
        Search properties based on query parameters
        
        Args:
            query: Property search query parameters (includes pagination)
            
        Returns:
            PropertySearchResultEntity with search results
        """
        try:
            logger.info(f"Searching properties with query: {query}")
            
            # Get properties from repository
            properties = await self.repository.search_properties(query)
            
            # Get total count for pagination
            total_count = await self.repository.get_properties_count(query)
            
            # Create result entity
            result = PropertySearchResultEntity(
                properties=properties,
                total_count=total_count,
                page=query.page,
                page_size=query.page_size
            )
            
            logger.info(f"Found {len(properties)} properties out of {total_count} total")
            return result
            
        except Exception as e:
            logger.error(f"Error searching properties: {str(e)}")
            raise

    def validate_search_query(self, query: PropertySearchQueryEntity) -> bool:
        """
        Validate search query parameters
        
        Args:
            query: Property search query parameters
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # If 'all' is True, only validate pagination parameters
            if query.all:
                logger.info("Validating 'all' properties query")
                return True
            
            # For filtered search, validate required parameters
            # Check if destination is provided
            if not query.destination or not query.destination.strip():
                logger.warning("Destination is required for property search")
                return False
            
            # Check if guests is provided and positive
            if query.guests is None or query.guests <= 0:
                logger.warning("Number of guests must be a positive integer")
                return False
            
            # Check if coordinates are valid when provided
            if query.latitude is not None and query.longitude is not None:
                if not (-90 <= query.latitude <= 90) or not (-180 <= query.longitude <= 180):
                    logger.warning("Invalid latitude or longitude coordinates")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating search query: {str(e)}")
            return False
