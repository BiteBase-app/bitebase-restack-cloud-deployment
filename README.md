# Restaurant BI System

A comprehensive Business Intelligence (BI) system for the restaurant industry, built with Restack AI and following SPEC-001 architecture.

## System Architecture

The system integrates multiple components for robust data processing and analysis:

- Vector Database (Weaviate) for semantic search and data embeddings
- Graph Database (Neo4j) for relationship analysis
- GraphRAG for enhanced data retrieval and analysis
- Redis for caching and real-time data processing
- Restack for AI workflow management

## Project Structure

```
.
├── apps/                     # Application source code
│   ├── backend/              # Backend application
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core system components
│   │   ├── functions.py      # Business logic
│   │   ├── monitoring/       # System monitoring
│   │   ├── workflows.py      # Workflow definitions
│   │   ├── agents.py         # Agent definitions
│   │   └── services.py       # Service management script
│   └── frontend/             # Frontend application
│       ├── src/              # Frontend source code
│       ├── public/           # Public assets
│       ├── pages/            # Next.js pages
│       ├── components/       # UI components
│       ├── styles/           # CSS styles
│       └── ...               # Other frontend files
├── docker/                   # Docker configurations
│   ├── Dockerfile            # Main application Dockerfile
│   └── Dockerfile.streamlit  # Dashboard Dockerfile
├── docs/                     # Documentation
│   └── SPEC-001.asciidoc     # System specifications
├── dags/                     # Airflow DAGs
│   └── scheduler.py          # Scheduler script
├── docker-compose.yml
└── requirements.txt
```

## Features

- Real-time data collection and analysis
- Semantic search capabilities via Weaviate
- Relationship-based analytics using Neo4j
- Enhanced data retrieval with GraphRAG
- Business intelligence dashboards
- MLOps infrastructure with monitoring
- Automated reporting and insights

## Prerequisites

- Docker and Docker Compose
- Restack AI account and API key
- At least 16GB RAM for running all services

## Environment Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd restaurant-bi-system
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Restack API key
```

3. Start the services:
```bash
docker-compose up -d
```

## Available Services

- Main Application: http://localhost:8000
  - API Documentation: http://localhost:8000/docs
  - Restack Developer UI: http://localhost:5233

- Databases:
  - Vector DB (Weaviate): http://localhost:8080
  - Graph DB (Neo4j): http://localhost:7474
  - GraphRAG: http://localhost:5000

- Visualization:
  - Business Intelligence Dashboard: http://localhost:8501

## Development

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black src/
```

## System Components

### Vector Database (Weaviate)
- Handles semantic search capabilities
- Stores embeddings for efficient similarity search
- Enables complex data queries

### Graph Database (Neo4j)
- Manages relationship data
- Enables complex pattern matching
- Supports business relationship analysis

### GraphRAG
- Enhances data retrieval
- Combines graph-based and vector-based search
- Improves analytics accuracy

### Redis
- Handles caching
- Supports real-time data processing
- Manages session data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License