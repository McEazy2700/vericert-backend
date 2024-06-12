from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    pguser: str = Field(default="")
    pgpassword: str = Field(default="")
    pghost: str = Field(default="")
    pgport: int = Field(default=0)
    pgdatabase: str = Field(default="")
    pinyata_api_key: str = Field(default="")
    pinyata_api_secret: str = Field(default="")
    pinyata_jwt: str = Field(default="")
    pinyata_gateway_url: str = Field(default="")
    allowed_origins: str = Field(default="")
    secret_key: str = Field(default="")
    algod_server: str = Field(default="")
    indexer_server: str = Field(default="")
    deployer_mnemonic: str = Field(default="")
    super_secret_phrase: str = Field(default="")
    frontend_base_url: str = Field(default="")
    smart_contract_application_id: int = Field(default=0)


settings = Settings()
