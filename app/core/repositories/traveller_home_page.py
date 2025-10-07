from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.entities.traveller.home_page import PropertySearchEntity, PropertySearchQueryEntity


class TravellerHomePageRepositoryInterface(ABC):
    """Interface for traveller home page repository operations"""

    @abstractmethod
    async def search_properties(
        self, 
        query: PropertySearchQueryEntity
    ) -> List[PropertySearchEntity]:
        """
        Search properties based on query parameters
        
        Args:
            query: Property search query parameters (includes pagination)
            
        Returns:
            List of PropertySearchEntity matching the search criteria
        """
        pass

    @abstractmethod
    async def get_properties_count(
        self, 
        query: PropertySearchQueryEntity
    ) -> int:
        """
        Get total count of properties matching search criteria
        
        Args:
            query: Property search query parameters
            
        Returns:
            Total count of matching properties
        """
        pass

    @abstractmethod
    def convert_lat_lng_to_geography(self, latitude: float, longitude: float) -> str:
        """
        Convert latitude and longitude to PostGIS geography point
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            PostGIS geography point string
        """
        pass

    @abstractmethod
    def parse_destination_hierarchy(self, destination: str) -> dict:
        """
        Parse destination string to extract location hierarchy
        
        Args:
            destination: Destination string from Mapbox
            
        Returns:
            Dictionary with parsed location components
        """
        pass
