from datetime import datetime, timedelta

from beanie.odm.operators.update.general import Set
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from mof.apienv import apienv
from mof.auth.constants import TokenType
from mof.auth.dto.login_dto import LoginDTO
from mof.auth.dto.login_response import LoginResponseDTO
from mof.auth.dto.refresh_token_res import RefreshTokenResponseDTO
from mof.auth.errors import auth_errors
from mof.auth.models.session_doc import SessionDocument
from mof.exceptions import APIException
from mof.user.dto.user_dto import UserDTO
from mof.user.errors import user_errors
from mof.user.services.user_service import user_service
from mof.auth.services.crypto_service import crypto_service


class AuthService:
    crypto_service = crypto_service
    user_service = user_service

    access_token_schema = OAuth2PasswordBearer(
        tokenUrl="login",
        scheme_name="Login",
    )

    refresh_token_schema = OAuth2PasswordBearer(
        tokenUrl="refresh",
        scheme_name="Refresh",
    )

    async def authenticate_user(self, dto: LoginDTO) -> LoginResponseDTO:
        user = await self.user_service.find_by_email(email=dto.email)
        if not user:
            raise APIException(error=user_errors.not_found)

        if not crypto_service.validate_password(dto.password, user.password):
            raise APIException(error=auth_errors.invalid_credentials)

        if user.deactivated:
            raise APIException(error=auth_errors.deactivated)

        user_dto = UserDTO.model_validate(user.model_dump()).model_dump()
        access_token = self.crypto_service.create_token(data=user_dto, token_type=TokenType.ACCESS_TOKEN)
        refresh_token = self.crypto_service.create_token(data=user.model_dump(), token_type=TokenType.REFRESH_TOKEN)

        session = SessionDocument.model_construct()
        session.user_id = user.id
        session.expires_at = datetime.utcnow() + timedelta(minutes=apienv.REFRESH_TOKEN_EXPIRATION)
        session.login_at = datetime.utcnow()
        session.last_seen_at = datetime.utcnow()
        session.refresh_token = refresh_token

        await session.insert()

        return LoginResponseDTO.model_validate({
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "user": user_dto,
        })

    async def refresh_token(self, token: str) -> RefreshTokenResponseDTO:
        user = self.crypto_service.verify_token(token=token, token_type=TokenType.REFRESH_TOKEN)

        user = await self.user_service.get_user(id=user.id)
        if not user:
            raise APIException(error=user_errors.not_found)
        if user.deactivated:
            raise APIException(error=auth_errors.deactivated)

        current_session = await SessionDocument.find_one({SessionDocument.refresh_token: token})

        if not current_session:
            raise APIException(error=auth_errors.no_session)

        if current_session.revoked:
            raise APIException(error=auth_errors.session_revoked)

        user_dto = UserDTO.model_validate(user.model_dump()).model_dump()
        access_token = self.crypto_service.create_token(data=user_dto, token_type=TokenType.ACCESS_TOKEN)

        if current_session:
            await current_session.update(Set({
                SessionDocument.last_seen_at: datetime.utcnow()
            }))

        return RefreshTokenResponseDTO.model_validate({
            "accessToken": access_token,
        })

    async def current_user(self, token: str = Depends(access_token_schema)) -> UserDTO:
        user = self.crypto_service.verify_token(token=token, token_type=TokenType.ACCESS_TOKEN)
        user = await self.user_service.get_user(id=user.id)

        if not user:
            raise APIException(error=user_errors.not_found)

        if user.deactivated:
            raise APIException(error=auth_errors.deactivated)

        return UserDTO.model_validate(user.model_dump())

    async def logout(self, token: str) -> None:
        session = await SessionDocument.find_one({SessionDocument.refresh_token: token})
        if session:
            await session.update(Set({
                SessionDocument.revoked: True,
                SessionDocument.logout_at: datetime.utcnow()
            }))


auth_service = AuthService()
