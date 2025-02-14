import os

# Backend API
BACKEND_API_URL = os.getenv('BACKEND_API_URL', 'http://backend:8000')

# AI Agent
AI_AGENT_URL = os.getenv('AI_AGENT_URL', 'http://ai-agent:8501')

# Vector DB
VECTOR_DB_URL = os.getenv('VECTOR_DB_URL', 'postgresql://user:password@vector-db:5432/vectorstore')

# Redis Cache
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379')

# Data Lake
DATALAKE_URL = os.getenv('DATALAKE_URL', 'http://datalake:9000')

# Streamlit Config
STREAMLIT_SERVER_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', '8501'))
STREAMLIT_SERVER_ADDRESS = os.getenv('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')