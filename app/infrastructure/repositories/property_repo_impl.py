from app.core.repositories import PropertyRepo
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.entities import PropertyDetailsEntity, PropertyOnlyDetailsEntity, PropertyUpdateEntity, PropertyAddressEntity
from app.infrastructure.database.models.onboard import Property, PropertyAddress, PropertyAmenities, PropertyImages
from app.infrastructure.database.models.onboard import Host
from sqlalchemy import insert, func, update, delete
from sqlalchemy.future import select
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)



class PropertyRepoImpl(PropertyRepo):
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session
    
    #add property main implementation
    async def add_property(self, property_data: PropertyDetailsEntity)->str | None:
        try:
            property_insert_query = insert(Property).values(
                host_id=int(property_data.host_id),
                max_guests = property_data.max_guests,
                bedrooms = property_data.bedrooms,
                price_per_night = property_data.price_per_night,
                property_name=property_data.property_name,
                property_type=property_data.property_type,
                property_description=property_data.property_description,
            ).returning(Property.id)

            property_result = await self.session.execute(property_insert_query)
            property_id = property_result.scalar_one()

            coordinates = property_data.property_address.coordinates
            point = None
            if coordinates and 'longitude' in coordinates and 'latitude' in coordinates:    
                point = f"POINT({coordinates['longitude']} {coordinates['latitude']})"
            
            address_insert_query = insert(PropertyAddress).values(
                property_id=property_id,
                house_name=property_data.property_address.house_name,  
                landmark=property_data.property_address.landmark,
                pincode=property_data.property_address.pincode,   
                district=property_data.property_address.district,
                state=property_data.property_address.state,
                country=property_data.property_address.country,
                location=point
            )
            await self.session.execute(address_insert_query)

            for img in property_data.property_images:
                image_insert_query = insert(PropertyImages).values(
                    property_id=property_id,
                    image_url=img.image_url,
                    is_primary=img.is_primary,
                    public_id=img.public_id
                )
                await self.session.execute(image_insert_query)
            
            for amenity in property_data.amenities:
                amenity_insert_query = insert(PropertyAmenities).values(
                    property_id=property_id,
                    amenity=amenity
                )
                await self.session.execute(amenity_insert_query)
            
            await self.session.commit()
            return str(property_id)
        except Exception as e:
            await self.session.rollback()
            return None

    async def get_host_id(self, user_id):
        result = await self.session.execute(
            select(Host.id).where(Host.user_id == int(user_id))
        )
        host_id = result.scalar_one_or_none()
        return host_id
    
    #helper methods for getting the property data
    async def _get_images_by_property_ids(self, property_ids):
        query = select(PropertyImages).where(PropertyImages.property_id.in_(property_ids))
        result = await self.session.execute(query)
        images_dict = {}
        for img in result.scalars():
            if img.property_id not in images_dict:
                images_dict[img.property_id] = []
            images_dict[img.property_id].append(img)
        return images_dict

    async def _get_amenities_by_property_ids(self, property_ids):
        query = select(PropertyAmenities).where(PropertyAmenities.property_id.in_(property_ids))
        result = await self.session.execute(query)
        amenities_dict = {}
        for amenity in result.scalars():
            if amenity.property_id not in amenities_dict:
                amenities_dict[amenity.property_id] = []
            amenities_dict[amenity.property_id].append(amenity.amenity)
        return amenities_dict 

    async def _get_addresses_by_property_ids(self, property_ids):
        """Get addresses with location as WKT text"""
        query = (
            select(
                PropertyAddress,
                func.ST_AsText(PropertyAddress.location).label('location_wkt')
            )
            .where(PropertyAddress.property_id.in_(property_ids))
        )
        result = await self.session.execute(query)
        
        addresses = {}
        for row in result:
            address = row.PropertyAddress
            addresses[address.property_id] = {
                'address': address,
                'location_wkt': row.location_wkt
            }
        return addresses

    def _extract_coordinates(self, address_data):
        """Extract coordinates from WKT string"""
        coordinates = {}
        if address_data and address_data.get('location_wkt'):
            wkt = address_data['location_wkt']
            print(f"DEBUG - WKT from query: {wkt}")
            
            if wkt.startswith('POINT('):
                # Remove 'POINT(' and ')' and split coordinates
                coords_str = wkt[6:-1]
                coords = coords_str.split()
                if len(coords) == 2:
                    coordinates = {
                        'longitude': float(coords[0]),
                        'latitude': float(coords[1])
                    }
                    print(f"DEBUG - Extracted coordinates: {coordinates}")
            else:
                print(f"DEBUG - WKT format unexpected: {wkt}")
        
        return coordinates

    #To fetch all the properties of a single host
    async def get_properties_by_host_id(self, host_id: int) -> List[PropertyOnlyDetailsEntity]:
        try:
            # Get basic property info
            properties_query = (
                select(Property)
                .where(Property.host_id == host_id)
            )
            properties_result = await self.session.execute(properties_query)
            properties = properties_result.scalars().all()
            
            if not properties:
                return []
            
            property_ids = [prop.id for prop in properties]
            
            # Use the new method that returns WKT
            addresses_data = await self._get_addresses_by_property_ids(property_ids)
            images_dict = await self._get_images_by_property_ids(property_ids)
            amenities_dict = await self._get_amenities_by_property_ids(property_ids)
            
            properties_list = []
            for property in properties:
                address_info = addresses_data.get(property.id)
                if not address_info:
                    continue
                
                address = address_info['address']
                
                property_data = {
                    'property_id': str(property.id),
                    'property_name': property.property_name,
                    'property_description': property.property_description,
                    'property_type': property.property_type,
                    'max_guests': property.max_guests,
                    'bedrooms': property.bedrooms,
                    'price_per_night': property.price_per_night,
                    'amenities': amenities_dict.get(property.id, []),
                    'property_address': {
                        'house_name': address.house_name,
                        'landmark': address.landmark,
                        'pincode': address.pincode,
                        'district': address.district,
                        'state': address.state,
                        'country': address.country,
                        'coordinates': self._extract_coordinates(address_info)  # Pass the address_info with WKT
                    },
                    'property_images': [
                        {
                            'image_url': img.image_url,
                            'is_primary': img.is_primary,
                            'public_id': img.public_id
                        }
                        for img in images_dict.get(property.id, [])
                    ]
                }
                
                property_entity = PropertyOnlyDetailsEntity(**property_data)
                properties_list.append(property_entity)
            
            return properties_list
            
        except Exception as e:
            print(f"Error fetching properties for host {host_id}: {str(e)}")
            return []
        

    async def get_property_by_id(self, property_id: int) -> Optional[PropertyOnlyDetailsEntity]:
        """Get a single property by its ID using existing helper methods"""
        try:
            # Use existing helper methods with single property ID
            property_ids = [property_id]
            
            # Batch fetch related data (works with single ID too)
            addresses_data = await self._get_addresses_by_property_ids(property_ids)
            images_dict = await self._get_images_by_property_ids(property_ids)
            amenities_dict = await self._get_amenities_by_property_ids(property_ids)
            
            # Get the main property
            property_query = select(Property).where(Property.id == property_id)
            property_result = await self.session.execute(property_query)
            property_obj = property_result.scalar_one_or_none()
            
            if not property_obj:
                return None
            
            address_info = addresses_data.get(property_id)
            if not address_info:
                return None
            
            address = address_info['address']
            
            property_data = {
                'property_id': str(property_obj.id),
                'property_name': property_obj.property_name,
                'property_description': property_obj.property_description,
                'property_type': property_obj.property_type,
                'max_guests': property_obj.max_guests,
                'bedrooms': property_obj.bedrooms,
                'price_per_night': property_obj.price_per_night,
                'amenities': amenities_dict.get(property_id, []),
                'property_address': {
                    'house_name': address.house_name,
                    'landmark': address.landmark,
                    'pincode': address.pincode,
                    'district': address.district,
                    'state': address.state,
                    'country': address.country,
                    'coordinates': self._extract_coordinates(address_info)
                },
                'property_images': [
                    {
                        'image_url': img.image_url,
                        'is_primary': img.is_primary,
                        'public_id': img.public_id
                    }
                    for img in images_dict.get(property_id, [])
                ]
            }
            
            return PropertyOnlyDetailsEntity(**property_data)
            
        except Exception as e:
            print(f"Error fetching property {property_id}: {str(e)}")
            return None

    async def update_property(self, property_id: str, property_data: PropertyUpdateEntity, host_id: int) -> bool:
        """Update a property with the given data using the PropertyUpdateEntity"""
        try:
            property_id_int = int(property_id)
            
            # First, verify the property belongs to the host
            if not await self._verify_property_ownership(property_id_int, host_id):
                return False
            
            # Update main property table using entity helper method
            await self._update_property_main_data(property_id_int, property_data)
            
            # Update address if provided
            if property_data.has_address_update():
                await self._update_property_address(property_id_int, property_data.property_address)
            
            # Update amenities if provided
            if property_data.has_amenities_update():
                await self._update_property_amenities(property_id_int, property_data.amenities)
            
            # Update images if provided
            if property_data.has_images_update():
                await self._update_property_images(property_id_int, property_data.property_images)
            
            await self.session.commit()
            logger.info(f"Successfully updated property {property_id}")
            return True
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error updating property {property_id}: {str(e)}")
            return False

    async def _verify_property_ownership(self, property_id: int, host_id: int) -> bool:
        """Verify that the property belongs to the host"""
        property_query = select(Property).where(
            Property.id == property_id,
            Property.host_id == host_id
        )
        property_result = await self.session.execute(property_query)
        existing_property = property_result.scalar_one_or_none()
        
        if not existing_property:
            logger.warning(f"Property {property_id} not found or doesn't belong to host {host_id}")
            return False
        return True

    async def _update_property_main_data(self, property_id: int, property_data: PropertyUpdateEntity):
        """Update the main property table fields"""
        update_data = property_data.get_update_data()
        
        # Filter out nested objects that are handled separately
        main_fields = {k: v for k, v in update_data.items() 
                      if k not in ['property_address', 'property_images', 'amenities']}
        
        if main_fields:
            property_update_query = update(Property).where(
                Property.id == property_id
            ).values(**main_fields)
            await self.session.execute(property_update_query)

    async def _update_property_address(self, property_id: int, address_data: PropertyAddressEntity):
        """Update property address"""
        address_update_data = {
            'house_name': address_data.house_name,
            'landmark': address_data.landmark or "",
            'pincode': address_data.pincode,
            'district': address_data.district,
            'state': address_data.state,
            'country': address_data.country
        }
        
        # Handle coordinates
        if address_data.coordinates:
            coordinates = address_data.coordinates
            if 'longitude' in coordinates and 'latitude' in coordinates:
                point = f"POINT({coordinates['longitude']} {coordinates['latitude']})"
                address_update_data['location'] = point
        
        address_update_query = update(PropertyAddress).where(
            PropertyAddress.property_id == property_id
        ).values(**address_update_data)
        await self.session.execute(address_update_query)

    async def _update_property_amenities(self, property_id: int, amenities: list):
        """Update property amenities by replacing all existing ones"""
        # Delete existing amenities
        delete_amenities_query = delete(PropertyAmenities).where(
            PropertyAmenities.property_id == property_id
        )
        await self.session.execute(delete_amenities_query)
        
        # Insert new amenities
        for amenity in amenities:
            amenity_insert_query = insert(PropertyAmenities).values(
                property_id=property_id,
                amenity=amenity
            )
            await self.session.execute(amenity_insert_query)

    async def _update_property_images(self, property_id: int, images: list):
        """Update property images by replacing all existing ones"""
        # Delete existing images
        delete_images_query = delete(PropertyImages).where(
            PropertyImages.property_id == property_id
        )
        await self.session.execute(delete_images_query)
        
        # Insert new images
        for img in images:
            image_insert_query = insert(PropertyImages).values(
                property_id=property_id,
                image_url=img.image_url,
                is_primary=img.is_primary,
                public_id=img.public_id
            )
            await self.session.execute(image_insert_query)