from app.core.repositories import UserRepository
from app.core.validations.types import StrictEmail
from app.core.entities import AdminCreationEntity


class CreateAdminUserUseCase:
    def __init__(
            self,
            user_repo: UserRepository
    ):
        self.user_repo = user_repo

    
    async def execute(
            self,
            email: StrictEmail,
            password: str,
            first_name: str,
            last_name: str
    )->bool:
        if not email or not password:
            raise ValueError("Email and password are required")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        existing_user = await self.user_repo.does_user_exist(email=email)
        if existing_user:
            raise ValueError("User with this email already exists")

        admin_data = AdminCreationEntity(
            email=email,
            password= password,
            first_name=first_name,
            last_name = last_name
        )
        
        return await self.user_repo.create_admin_user(admin_data = admin_data)
