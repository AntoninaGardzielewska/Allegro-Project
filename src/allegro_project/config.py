from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    allegro_client_auth: str
    allegro_client_secret: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )