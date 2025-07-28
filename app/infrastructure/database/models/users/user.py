from app.infrastructure.database.session import Base
from sqlalchemy import Column, Integer, Text, Boolean, DateTime
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, autoincrement = True)
    full_name = Column(Text, nullable= False)
    email = Column(Text, unique = True, nullable= False)
    phone_number = Column(Integer, nullable = True)
    password_hash = Column(Text)
    profile_image = Column(Text)
    is_admin = Column(Boolean, default = False)
    is_guide = Column(Boolean, default = False)
    is_traveller = Column(Boolean, default= True)
    is_active = Column(Boolean, default = True)
    created_at = Column(DateTime, server_default = func.now())
    updated_at = Column(DateTime, server_default = func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User {self.email}>"