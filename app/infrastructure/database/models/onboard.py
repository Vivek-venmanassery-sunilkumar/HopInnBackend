from app.infrastructure.database.session import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func, Numeric, TEXT
from geoalchemy2 import Geography
from sqlalchemy import UniqueConstraint

class Guide(Base):
    __tablename__ = 'guide'

    id = Column(Integer, primary_key = True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    bio = Column(String(255), nullable=False)
    profession=Column(String(255), nullable=False)
    expertise=Column(String(255), nullable=False)
    hourly_rate = Column(String(255), nullable=False)
    house_name = Column(String(255), nullable=False)
    landmark = Column(String(255), nullable = True)
    pincode = Column(String(255), nullable=False)
    district = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=True)
    is_blocked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class Languages(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable = False)
    language = Column(String(255), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'language', name='uq_user_language'),
    )

class Host(Base):
    __tablename__ = 'host'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    about = Column(String(255), nullable=False)
    profession = Column(String(255), nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class Property(Base):
    __tablename__ = 'property'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(Integer, ForeignKey('host.id', ondelete='CASCADE'), nullable=False)
    property_name = Column(String(255), nullable=False)
    property_description = Column(TEXT, nullable=False)
    child_friendly = Column(Boolean, default=False, nullable=False)
    max_guests = Column(Integer, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    price_per_night = Column(Numeric(10,2), nullable=False)
    property_type = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class PropertyImages(Base):
    __tablename__ = 'property_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey('property.id', ondelete='CASCADE'), nullable=False)
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    public_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class PropertyAddress(Base):
    __tablename__ = 'property_address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey('property.id', ondelete='CASCADE'), nullable=False)
    house_name = Column(String(255), nullable=False)
    landmark = Column(String(255), nullable = True)
    pincode = Column(String(255), nullable=False)
    district = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=True)

class PropertyAmenities(Base):
    __tablename__ = 'property_amenities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey('property.id', ondelete='CASCADE'), nullable=False)
    amenity = Column(String(100), nullable=False)
