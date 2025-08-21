from abc import ABC, abstractmethod

class EmailRepo(ABC):
    #Core abstraction for email sending
    @abstractmethod
    def send(self, email: str, otp: str)-> None:
        pass