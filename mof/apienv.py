import os
import sys

from pydantic import Field
from pydantic_settings import BaseSettings


def get_env():
    if "pytest" in "".join(sys.argv):
        return ".env.test"
    elif os.environ.get("ENV", "development") == "development":
        return ".env.dev"
    elif os.environ.get("ENV", "test"):
        return ".env.test"
    else:
        return ".env"


class ApiEnv(BaseSettings):
    # General
    Environment: str = Field(
        "development",
        env="ENV",
        description="Runtime environment.",
    )

    # Security
    ACCESS_TOKEN_PRIVATE_KEY: str = Field(
        ...,
        env="ACCESS_TOKEN_PRIVATE_KEY",
        description="Access token private key.",
    )
    ACCESS_TOKEN_PUBLIC_KEY: str = Field(
        ...,
        env="ACCESS_TOKEN_PUBLIC_KEY",
        description="Access token public key.",
    )
    ACCESS_TOKEN_EXPIRATION: int = Field(
        ...,
        env="ACCESS_TOKEN_EXPIRATION",
        description="Access token expiration in seconds.",
    )

    REFRESH_TOKEN_PRIVATE_KEY: str = Field(
        ...,
        env="REFRESH_TOKEN_PRIVATE_KEY",
        description="Refresh token private key.",
    )
    REFRESH_TOKEN_PUBLIC_KEY: str = Field(
        ...,
        env="REFRESH_TOKEN_PUBLIC_KEY",
        description="Refresh token public key.",
    )
    REFRESH_TOKEN_EXPIRATION: int = Field(
        ...,
        env="REFRESH_TOKEN_EXPIRATION",
        description="Refresh token expiration in seconds.",
    )

    # Database
    DB_USER: str = Field(
        ...,
        env="DB_USER",
        description="Database user.",
    )
    DB_PASS: str = Field(
        ...,
        env="DB_PASS",
        description="Database password.",
    )
    DB_HOST: str = Field(
        ...,
        env="DB_HOST",
        description="Database host.",
    )
    DB_NAME: str = Field(
        ...,
        env="DB_NAME",
        description="Database name.",
    )

    class Config:
        env_file = get_env()
        env_encoding = "utf-8"
        extra = "ignore"


apienv = ApiEnv()
