from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс настроек

    Атрибуты
    --------
    DB_HOST: str
        адрес хоста сервера
    DB_PORT: int
        порт
    DB_USER: str
        имя пользователя
    DB_PASS: str
        пароль пользователя
    DB_NAME: str
        имя базы данных

    MODE: Literal["DEV", "TEST", "PROD"]  # default DEV, test activating for start tests
        режим запуска
    LOG_LEVEL: str
        режим логгирования
    """

    model_config = SettingsConfigDict(env_file=".env")

    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: Optional[str] = None
    TEST_DB_PORT: Optional[int] = None
    TEST_DB_USER: Optional[str] = None
    TEST_DB_PASS: Optional[str] = None
    TEST_DB_NAME: Optional[str] = None

    ORIGINS: str


settings = Settings()
