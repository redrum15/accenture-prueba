from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    database_url: str = "sqlite:///./chat_messages.db"

    app_name: str = "Message Processing API"
    app_version: str = "1.0.0"
    debug: bool = True

    default_page_size: int = 10
    max_page_size: int = 100

    inappropriate_words: list[str] = ["bad", "inappropriate", "prohibited", "censored"]

    class Config:
        env_file = ".env"


settings = Settings()
