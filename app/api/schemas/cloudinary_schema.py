from pydantic import BaseModel

class CloudData(BaseModel):
    cloudName: str
    apiKey: str
    timestamp: int
    signature: str
