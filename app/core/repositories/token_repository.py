from abc import ABC, abstractmethod

class TokenRepository(ABC):
    @abstractmethod
    def generate_access_token(self, user_id: str)->str:
        pass
    
    @abstractmethod
    def generate_refresh_token(self, user_id: str)->str:
        pass

    @abstractmethod
    def verify_access_token(self, token: str)->dict | None:
        pass

    @abstractmethod
    def decode_token(self, token: str)->dict | None:
        pass

    @abstractmethod
    def verify_refresh_token(self, token: str)->dict | None:
        pass