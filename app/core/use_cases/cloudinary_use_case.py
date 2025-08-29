import time
import cloudinary.utils
import cloudinary.uploader
from app.config.cloudinary import cloud_config
from app.api.schemas import CloudDataSchema

class CloudinaryUseCase:
    @staticmethod
    def generate_upload_signature()->CloudDataSchema:
        timestamp = int(time.time())

        params = {
            'timestamp': timestamp
        }
        
        #we need not need to pass in anything because we have already configured cloud_config
        signature = cloudinary.utils.api_sign_request(
            params_to_sign=params,
            api_secret=cloud_config.api_secret
            )

        return CloudDataSchema(
            cloudName=cloud_config.cloud_name,
            apiKey=cloud_config.api_key,
            timestamp=timestamp,
            signature=signature
        )
    
    @staticmethod
    def delete_profile_image(public_id: str)->bool:
        try:
            result = cloudinary.uploader.destroy(public_id)

            if result.get("result")=='ok':
                return True
            else:
                return False
        except Exception as e:
            return False