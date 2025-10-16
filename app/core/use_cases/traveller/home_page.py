from typing import List
from app.core.entities.traveller.home_page import PropertySearchEntity, PropertySearchQueryEntity, PropertySearchResultEntity, GuideSearchEntity, GuideSearchQueryEntity, GuideSearchResultEntity
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


    async def search_guides(
        self, 
        query: GuideSearchQueryEntity
    ) -> GuideSearchResultEntity:
        """
        Search guides based on query parameters
        
        Args:
            query: Guide search query parameters (includes pagination)
            
        Returns:
            GuideSearchResultEntity with search results
        """
        try:
            logger.info(f"Searching guides with query: {query}")
            
            # Get guides from repository
            guides = await self.repository.search_guides(query)
            
            # Get total count for pagination
            total_count = await self.repository.get_guides_count(query)
            
            # Create result entity
            result = GuideSearchResultEntity(
                guides=guides,
                total_count=total_count,
                page=query.page,
                page_size=query.page_size
            )
            
            logger.info(f"Found {len(guides)} guides out of {total_count} total")
            return result
            
        except Exception as e:
            logger.error(f"Error searching guides: {str(e)}")
            raise

