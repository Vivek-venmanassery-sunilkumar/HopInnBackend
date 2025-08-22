import time
import cloudinary
import cloudinary.utils
from app.config.cloudinary import cloud_config
from app.api.schemas import CloudData

class CloudinaryUseCase:
    @staticmethod
    def generate_upload_signature()->CloudData:
        timestamp = int(time.time())

        params = {
            'timestamp': timestamp
        }

        signature = cloudinary.utils.api_sign_request(
            params_to_sign=params,
            api_secret=cloud_config.api_secret
        )

        return CloudData(
            cloudName=cloud_config.cloud_name,
            apiKey=cloud_config.api_key,
            timestamp=timestamp,
            signature=signature
        )