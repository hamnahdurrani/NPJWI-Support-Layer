from pydantic_settings import BaseSettings
 
class Config(BaseSettings):
    listen_port: int = 8090
    npjwi_timeout: int = 25
    npjwi_base_url: str = "/evaluation"
    env_routing: dict = {
        "dev": "https://npka-npjwi-dev.inago.com/nextgen",
    }
 
config = Config()