from app.infrastructure.database.session import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from geoalchemy2 import Geography

class Guide(Base):
    __tablename__ = 'guide'

    id = Column(Integer, primary_key = True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    bio = Column(String(255), nullable=False)
    dob = Column(String(255), nullable=False)
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



class Languages(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    guide_id = Column(Integer, ForeignKey('guide.id', ondelete='CASCADE'), nullable = False)
    language = Column(String(255), nullable=False)