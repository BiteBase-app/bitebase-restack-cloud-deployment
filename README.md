# Restaurant BI System

A comprehensive Business Intelligence (BI) system for the restaurant industry, built with Restack AI and following SPEC-001 architecture.

## Project Structure

```
.
├── dags/                      # Airflow DAG definitions
│   └── scheduler.py
├── docker/                    # Docker configurations
│   ├── Dockerfile
│   └── Dockerfile.streamlit
├── docs/                      # Documentation
│   └── SPEC-001.asciidoc
├── src/
│   └── restaurant_bi/
│       ├── api/              # API endpoints
│       │   └── api_endpoints.py
│       ├── core/             # Core system components
│       │   ├── data_pipeline.py
│       │   ├── mlops_infrastructure.py
│       │   ├── restack_workflow.py
│       │   └── services.py
│       ├── dashboard/        # Streamlit dashboard
│       │   └── bi_dashboard.py
│       ├── functions/        # Business logic
│       │   └── functions.py
│       ├── monitoring/       # System monitoring
│       │   └── monitoring.py
│       └── workflows/        # Workflow definitions
│           └── workflows.py
├── docker-compose.yml
└── requirements.txt
```

## Features

- Real-time data collection and analysis
- Market trend analysis and competitor tracking
- Customer sentiment analysis
- Menu optimization
- Business intelligence dashboards
- MLOps infrastructure with monitoring
- Automated reporting and insights

## Prerequisites

- Docker and Docker Compose
- Restack AI account and API key
- Python 3.11+

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd restaurant-bi-system
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Restack API key and other configurations
```

3. Start the services:
```bash
docker-compose up -d
```

## Accessing Services

- Restack Developer UI: http://localhost:5233
- API Documentation: http://localhost:8000/docs
- Business Intelligence Dashboard: http://localhost:8501
- MLflow UI: http://localhost:5000
- Airflow UI: http://localhost:8080

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License