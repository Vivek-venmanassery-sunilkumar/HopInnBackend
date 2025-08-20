from abc import ABC, abstractmethod

class RedisRepoInterface(ABC):
    @abstractmethod
    async def store_signup_data(self,email: str, otp: str, user_data: dict)->None:
        pass

    @abstractmethod
    async def get_signup_data(self, email:str)->dict | None:
        pass

    @abstractmethod
    async def delete_signup_data(self, email: str)->None:
        pass

    @abstractmethod
    async def update_signup_data(self, email: str, **updates)->None:
        pass


    @abstractmethod
    async def store_blacklisted_token(self, token:str, expiry:int)->None:
        pass

    @abstractmethod
    async def is_token_blacklisted(self, token:str)->bool:
        pass
    


    


    
