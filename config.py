from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    listen_port: int = 8090
    npjwi_timeout: int = 25
    npjwi_base_url: str = "https://npka-npjwi-dev.inago.com/nextgen/evaluation"
    env_routing: dict = {
        "dev": "https://npka-npjwi-dev.inago.com/nextgen/evaluation",
    }

    class Config:
        env_file = ".env"

settings = Settings()