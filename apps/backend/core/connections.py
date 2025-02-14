import os
import redis
from sqlalchemy import create_engine
import minio
import aiohttp
from typing import Optional

# Database connections
def get_db_engine():
    return create_engine(os.getenv('DATABASE_URL'))

def get_vector_db_engine():
    return create_engine(os.getenv('VECTOR_DB_URL'))

# Redis connection
def get_redis_client():
    return redis.from_url(os.getenv('REDIS_URL', 'redis://redis:6379'))

# MinIO connection
def get_minio_client():
    return minio.Minio(
        os.getenv('DATALAKE_URL', 'datalake:9000').replace('http://', ''),
        access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
        secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin'),
        secure=False
    )

# Airflow connection
async def get_airflow_client():
    return await aiohttp.ClientSession().get(
        f"{os.getenv('AIRFLOW_URL', 'http://airflow:8080')}/api/v1/dags"
    )

# AI Agent connection
async def get_ai_agent_client(session: Optional[aiohttp.ClientSession] = None):
    if not session:
        session = aiohttp.ClientSession()
    return session, os.getenv('AI_AGENT_URL', 'http://ai-agent:8501')

# Prometheus metrics
async def get_prometheus_client(session: Optional[aiohttp.ClientSession] = None):
    if not session:
        session = aiohttp.ClientSession()
    return session, os.getenv('PROMETHEUS_URL', 'http://prometheus:9090')