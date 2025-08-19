from abc import ABC, abstractmethod

class TokenRepository(ABC):
    @abstractmethod
    def generate_access_token(self, email_id: str)->str:
        pass

    
    @abstractmethod
    def generate_refresh_token(self, email_id: str)->str:
        pass