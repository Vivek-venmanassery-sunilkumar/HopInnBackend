from app.infrastructure.database.session import Base
from sqlalchemy import Column, Integer, Boolean, DateTime, String, ForeignKey, Date
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, autoincrement = True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), unique = True, nullable= False)
    phone_number = Column(String(20), nullable = True)
    password_hash = Column(String(255))
    dob = Column(Date, nullable=True)
    profile_image = Column(String(500), nullable=True)
    profile_image_public_id = Column(String(255), nullable = True)
    google_id = Column(String(100), unique= True, nullable= True)
    is_admin = Column(Boolean, default = False)
    is_guide = Column(Boolean, default = False)
    is_traveller = Column(Boolean, default= True)
    is_active = Column(Boolean, default = True)
    created_at = Column(DateTime, server_default = func.now())
    updated_at = Column(DateTime, server_default = func.now(), onupdate=func.now())
    is_host = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User {self.email}>"


class UserKyc(Base):
    __tablename__ = 'kyc_docs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    kyc_image_url = Column(String(255))
    kyc_image_public_id = Column(String(255))
    verification_status = Column(String(20), default='pending')
    rejection_reason = Column(String(200), nullable=True)
    created_at = Column(DateTime, server_default = func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())