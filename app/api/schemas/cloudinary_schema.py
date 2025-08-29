from pydantic import BaseModel

class CloudDataSchema(BaseModel):
    cloudName: str
    apiKey: str
    timestamp: int
    signature: str
