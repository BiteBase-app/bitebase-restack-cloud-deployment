from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from typing import Dict, Any

from src.functions.data_collection import (
    collect_pos_data,
    collect_inventory_data,
    collect_customer_feedback,
    collect_external_data
)
from src.functions.market_analysis import (
    analyze_market_trends,
    analyze_competitor_data
)
from src.functions.bi_analytics import (
    generate_executive_insights,
    generate_operational_metrics
)

# Default DAG arguments
default_args = {
    'owner': 'restaurant_bi',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Data Collection DAG
data_collection_dag = DAG(
    'data_collection_pipeline',
    default_args=default_args,
    description='Daily data collection pipeline',
    schedule_interval='0 0 * * *',  # Run daily at midnight
    catchup=False
)

collect_pos = PythonOperator(
    task_id='collect_pos_data',
    python_callable=collect_pos_data,
    dag=data_collection_dag
)

collect_inventory = PythonOperator(
    task_id='collect_inventory_data',
    python_callable=collect_inventory_data,
    dag=data_collection_dag
)

collect_feedback = PythonOperator(
    task_id='collect_customer_feedback',
    python_callable=collect_customer_feedback,
    dag=data_collection_dag
)

collect_external = PythonOperator(
    task_id='collect_external_data',
    python_callable=collect_external_data,
    dag=data_collection_dag
)

# Set task dependencies
collect_pos >> collect_inventory >> collect_feedback >> collect_external

# Market Analysis DAG
market_analysis_dag = DAG(
    'market_analysis_pipeline',
    default_args=default_args,
    description='Weekly market analysis pipeline',
    schedule_interval='0 0 * * 0',  # Run weekly on Sunday
    catchup=False
)

analyze_market = PythonOperator(
    task_id='analyze_market_trends',
    python_callable=analyze_market_trends,
    dag=market_analysis_dag
)

analyze_competitors = PythonOperator(
    task_id='analyze_competitor_data',
    python_callable=analyze_competitor_data,
    dag=market_analysis_dag
)

# Set task dependencies
analyze_market >> analyze_competitors

# Business Intelligence DAG
bi_analysis_dag = DAG(
    'bi_analysis_pipeline',
    default_args=default_args,
    description='Hourly business intelligence pipeline',
    schedule_interval='0 * * * *',  # Run hourly
    catchup=False
)

generate_insights = PythonOperator(
    task_id='generate_executive_insights',
    python_callable=generate_executive_insights,
    dag=bi_analysis_dag
)

generate_metrics = PythonOperator(
    task_id='generate_operational_metrics',
    python_callable=generate_operational_metrics,
    dag=bi_analysis_dag
)

# Set task dependencies
generate_insights >> generate_metrics

# Menu Optimization DAG (runs nightly)
menu_optimization_dag = DAG(
    'menu_optimization_pipeline',
    default_args=default_args,
    description='Nightly menu optimization pipeline',
    schedule_interval='0 2 * * *',  # Run at 2 AM daily
    catchup=False
)

def optimize_menu(**context):
    """Optimize menu based on daily sales and inventory data"""
    # Implement menu optimization logic
    pass

menu_optimization = PythonOperator(
    task_id='optimize_menu',
    python_callable=optimize_menu,
    dag=menu_optimization_dag
)

# Model Retraining DAG (runs monthly)
model_retraining_dag = DAG(
    'model_retraining_pipeline',
    default_args=default_args,
    description='Monthly model retraining pipeline',
    schedule_interval='0 0 1 * *',  # Run on the 1st of each month
    catchup=False
)

def retrain_models(**context):
    """Retrain ML models with new data"""
    # Implement model retraining logic
    pass

model_retraining = PythonOperator(
    task_id='retrain_models',
    python_callable=retrain_models,
    dag=model_retraining_dag
)

# Data Quality Monitoring DAG
data_quality_dag = DAG(
    'data_quality_monitoring',
    default_args=default_args,
    description='Daily data quality monitoring pipeline',
    schedule_interval='0 1 * * *',  # Run at 1 AM daily
    catchup=False
)

def monitor_data_quality(**context):
    """Monitor data quality metrics"""
    # Implement data quality monitoring logic
    pass

data_quality_check = PythonOperator(
    task_id='monitor_data_quality',
    python_callable=monitor_data_quality,
    dag=data_quality_dag
)

# System Health Monitoring DAG
health_monitoring_dag = DAG(
    'system_health_monitoring',
    default_args=default_args,
    description='System health monitoring pipeline',
    schedule_interval='*/15 * * * *',  # Run every 15 minutes
    catchup=False
)

def check_system_health(**context):
    """Check system health metrics"""
    # Implement health monitoring logic
    pass

health_check = PythonOperator(
    task_id='check_system_health',
    python_callable=check_system_health,
    dag=health_monitoring_dag
)