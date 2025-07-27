from pydantic_settings import BaseSettings
from  pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    APP_ENV: str = Field('development', env='APP_ENV')
    
    class config:
        env_file = '.env'
        extra='ignore'
Settings=Settings()        