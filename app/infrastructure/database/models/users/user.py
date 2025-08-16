from app.infrastructure.database.session import Base
from sqlalchemy import Column, Integer, Boolean, DateTime, String
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, autoincrement = True)
    full_name = Column(String(100), nullable= False)
    email = Column(String(255), unique = True, nullable= False)
    phone_number = Column(String(20), nullable = True)
    password_hash = Column(String(255))
    profile_image = Column(String(500))
    google_id = Column(String(100), unique= True, nullable= True)
    is_admin = Column(Boolean, default = False)
    is_guide = Column(Boolean, default = False)
    is_traveller = Column(Boolean, default= True)
    is_active = Column(Boolean, default = True)
    created_at = Column(DateTime, server_default = func.now())
    updated_at = Column(DateTime, server_default = func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User {self.email}>"