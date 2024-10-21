import asyncpg
import os
import httpx
import logging
from enum import Enum
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from fastapi_offline import FastAPIOffline
from fastapi import FastAPI
from typing import Any, Dict, List, Tuple, Optional

debug: str = os.getenv('FASTAPI_DEBUG') # TURN OFF DEBUG ON PROD !!!
apikey: str = os.getenv('FASTAPI_KEY')
pg_conn: str = os.getenv('POSTGRES_DSN')

SECRET_VALUE: str = apikey       # CHANGE ME ON PROD !!!
SECRET_HEADER: str = 'X-API-Key'


docs_title: str = 'Keenetic API'
docs_description: str = 'Не лезь, убьёт!'

class Tags(Enum):
    keenetic = "Keenetic"


def auth401():
    X_API_KEY = APIKeyHeader(name=SECRET_HEADER)

    def api_key_auth(x_api_key: str = Depends(X_API_KEY)):
        if x_api_key != SECRET_VALUE:
            raise HTTPException(status_code=401, detail="Invalid API Key")

    auth_dep = [Depends(api_key_auth)]
    return auth_dep

def api_init():
    """
    Инициализирует и возвращает экземпляр FastAPI с учетом режима отладки.

    Args:
        debug (bool): Флаг, указывающий, находится ли приложение в режиме отладки.
        docs_title (str): Заголовок документации API.
        docs_description (str): Описание документации API.

    Returns:
        FastAPI: Экземпляр FastAPI с соответствующими настройками.
    """
    if debug == "TRUE":
        app = FastAPIOffline(
            title=docs_title,
            description=docs_description
        )
        logging.info("FastAPI app initialized in debug mode.")
    else:
        app = FastAPIOffline(
        # docs_url = None, # Disable docs (Swagger UI)
        # redoc_url = None, # Disable redoc
        dependencies = auth401(),
        title = docs_title,
        description = docs_description,
        )

    return app

# asyncpg wrapper

class PostgreSQL():
    def __init__(self):
        self.pool = None

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(pg_conn)
            return self

    async def disconnect(self):
        if self.pool is not None:
            await self.pool.close()
            self.pool = None

    async def execute(self, query: str, args = ()):
        await self.connect()

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, *args)

    async def fetch(self, query: str, *args: Any, count: int = 1, cache: bool = False):
        await self.connect()

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                async for record in connection.cursor(query, *args):
                    if count == 1:
                        return dict(record)
                return None

    async def fetchall(self, query: str, args = ()):
        await self.connect()
        
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                return await connection.fetch(query, *args)
    
    async def fetchval(self, query: str, *args: Any):
        await self.connect()

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchval(query, *args)  # Используем fetchval
                return result
