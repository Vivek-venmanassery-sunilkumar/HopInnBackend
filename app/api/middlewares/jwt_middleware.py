from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional, Callable
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.core.redis.redis_repo import RedisRepoInterface
from app.core.repositories.token.token_repository import TokenRepository


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(
            self, 
            app,
            token_repo: TokenRepository,
            redis_repo: RedisRepoInterface,
            exempt_paths: Optional[list]= None
            ):
        super().__init__(app)
        self.token_repo = token_repo
        self.redis_repo = redis_repo
        self.exempt_paths = exempt_paths or []
    
    def is_exempt_path(self, path:str)->bool:
        """Check if path should be exempt from JWT verification"""
        return any(path.startswith(exempt_path) for exempt_path in self.exempt_paths)
    
    async def verify_access_token(self, token:str)->Optional[dict]:
        """Verify JWT token and return payload if valid"""
        if not token:
            return None

        if await self.redis_repo.is_token_blacklisted(token):
            return None
        
        return self.token_repo.verify_access_token(token)
    
    async def extract_user_id(self, token: str)->Optional[str]:
        """Extract user_id from JWT token"""
        payload = self.token_repo.decode_token(token)
        if payload and 'user_id' in payload:
            return payload['user_id']
    
    async def dispatch(self, request: Request, call_next: Callable):
        #skip middleware for exempt paths
        if self.is_exempt_path(request.url.path):
            return await call_next(request)
        
        #Extract token from cookies 
        token = request.cookies.get("access_token")
        if not token:
            return JSONResponse(
                status_code=401,
                content={'detail':'Invalid or expired token'}
            )
        #Verify token
        payload = await self.verify_access_token(token)
        if not payload:
            return JSONResponse(
                status_code=401,
                content={'detail': 'Invalid or expired token'}
            )

        #extract user_id
        user_id = await self.extract_user_id(token)
        if not user_id:
            return JSONResponse(
                status_code = 401,
                content={'detail': 'Invalid token payload'}
            )
        
        #Add user_id and token paylod to request state
        request.state.user_id = user_id
        request.state.token_payload = payload
        request.state.token = token
        response = await call_next(request)
        return response
        