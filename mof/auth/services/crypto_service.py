import re
import uuid
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from mof.apienv import apienv
from mof.auth.constants import TokenType
from mof.auth.errors import auth_errors
from mof.exceptions import APIException
from mof.user.dto.user_dto import UserDTO


class CryptoService:
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    algorithm = "RS256"

    def hash_password(self, password: str) -> str:
        return self.context.hash(password)

    def validate_password(self, password: str, hashed_password: str) -> bool:
        return self.context.verify(password, hashed_password)

    def create_token(self, data: dict, token_type: TokenType) -> str:
        to_encode = data.copy()
        private_key = None
        expiration = None

        if token_type == TokenType.ACCESS_TOKEN:
            private_key = apienv.ACCESS_TOKEN_PRIVATE_KEY
            expiration = apienv.ACCESS_TOKEN_EXPIRATION
        elif token_type == TokenType.REFRESH_TOKEN:
            private_key = apienv.REFRESH_TOKEN_PRIVATE_KEY
            expiration = apienv.REFRESH_TOKEN_EXPIRATION

        expire = datetime.utcnow() + timedelta(minutes=expiration)
        to_encode.update({
            "exp": expire.timestamp(),
            "token_type": token_type.value
        })

        for key, value in to_encode.items():
            if isinstance(value, uuid.UUID) or isinstance(value, datetime):
                to_encode[key] = str(value)

        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=private_key,
            algorithm=self.algorithm,
        )

        return encoded_jwt

    def verify_token(self, token: str, token_type: TokenType) -> UserDTO:
        public_key = None

        if token_type == TokenType.ACCESS_TOKEN:
            public_key = apienv.ACCESS_TOKEN_PUBLIC_KEY
        elif token_type == TokenType.REFRESH_TOKEN:
            public_key = apienv.REFRESH_TOKEN_PUBLIC_KEY

        try:
            payload = jwt.decode(
                jwt=token,
                key=public_key,
                algorithms=[self.algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise APIException(auth_errors.expired_token)
        except jwt.InvalidTokenError:
            raise APIException(auth_errors.invalid_token)

        return UserDTO.model_validate(payload)



crypto_service = CryptoService()
