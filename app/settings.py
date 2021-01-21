from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "fast-api-postgre-hw"
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql://postgres:0000@localhost:5432/fast-api-postgre-hw"
    # AuthJWT
    access_token_expired_minutes: int = 30
    authjwt_secret_key: str = (
        "8087ae2e8f8df45cfa05ea70492a30733acee81e4112d3e9ea943207c378be5c"
    )
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}


settings = Settings()
