"""Configurações centrais do backend.

Este arquivo existe para concentrar tudo que pode variar por ambiente:
- URL do banco
- nome da aplicação
- modo debug

A ideia é simples: quando o projeto crescer, ninguém precisa sair caçando
configuração espalhada em 12 arquivos. O coração mora aqui.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Radar de Proventos"
    debug: bool = True
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/radar_proventos"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
