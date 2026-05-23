import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    # Bot tokeningiz xavfsiz holatda
    BOT_TOKEN: SecretStr = SecretStr(os.getenv("BOT_TOKEN", "8645488539:AAEtUvC9KcezHafzkEDoKs1ABJhFvNELDfU"))
    
    # Bot dasturchisi ID raqami
    ADMIN_ID: int = int(os.getenv("ADMIN_ID", "000000000"))

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )

config = Settings()