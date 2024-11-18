# import jwt
# from datetime import datetime, timedelta
from src.user.application.interfaces.login import AuthServiceInterface


class UserService(AuthServiceInterface):
    def generate_token(self, *, user_id: int) -> str:
        # payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=1)}
        # return jwt.encode(payload, "secret_key", algorithm="HS256")
        return "myawsomepassword"
