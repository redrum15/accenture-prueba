from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    database_url = "sqlite:///./chat_messages.db"

    app_name = "Message Processing API"
    app_version = "1.0.0"
    debug = True

    default_page_size = 10
    max_page_size = 100

    inappropriate_words = ["bad", "inappropriate", "prohibited", "censored"]

    class Config:
        env_file = ".env"


settings = Settings()
