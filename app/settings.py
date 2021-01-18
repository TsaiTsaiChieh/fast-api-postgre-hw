from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "fast-api-postgre-hw"
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql://postgres:0000@localhost:5432/fast-api-postgre-hw"
    # jwt settings
    # to get a string like this run: openssl rand -hex 32
    secret_key: str = "8087ae2e8f8df45cfa05ea70492a30733acee81e4112d3e9ea943207c378be5c"
    algorithm: str = "HS256"
    access_token_expired_minutes: int = 30
    
settings = Settings()

