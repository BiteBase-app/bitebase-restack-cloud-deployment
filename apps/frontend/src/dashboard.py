from typing import Dict, List, Any
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from jinja2 import Template
import streamlit as st
import aiohttp
import asyncio
import json
from . import config

class ExecutiveDashboard:
    def __init__(self):
        self.metrics = {}
        self.insights = []
        self.alerts = []

    def update_metrics(self, new_metrics: Dict[str, float]):
        """Update dashboard metrics"""
        self.metrics.update({
            'timestamp': datetime.now().isoformat(),
            **new_metrics
        })

    def generate_insights(self, data: Dict[str, Any]) -> List[str]:
        """Generate automated insights using NLP"""
        insights = []
        
        # Revenue insights
        if 'revenue' in data:
            trend = self.analyze_trend(data['revenue'])
            insights.append(f"Revenue is {trend['direction']} by {trend['percentage']}%")
        
        # Customer insights
        if 'customer_satisfaction' in data:
            sat_trend = self.analyze_trend(data['customer_satisfaction'])
            insights.append(f"Customer satisfaction is {sat_trend['direction']} by {sat_trend['percentage']}%")
        
        # Market position insights
        if 'market_share' in data:
            market_trend = self.analyze_trend(data['market_share'])
            insights.append(f"Market share is {market_trend['direction']} by {market_trend['percentage']}%")
        
        self.insights = insights
        return insights

    def analyze_trend(self, data: List[float]) -> Dict[str, Any]:
        """Analyze trend in time series data"""
        if len(data) < 2:
            return {'direction': 'unchanged', 'percentage': 0}
        
        change = ((data[-1] - data[0]) / data[0]) * 100
        direction = 'increasing' if change > 0 else 'decreasing'
        
        return {
            'direction': direction,
            'percentage': abs(round(change, 2))
        }

    def create_visualizations(self) -> Dict[str, go.Figure]:
        """Create dashboard visualizations"""
        figs = {}
        
        # Revenue trend
        if 'revenue' in self.metrics:
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=self.metrics['revenue'], name='Revenue'))
            figs['revenue_trend'] = fig
        
        # Customer satisfaction
        if 'customer_satisfaction' in self.metrics:
            fig = go.Figure()
            fig.add_trace(go.Bar(y=self.metrics['customer_satisfaction'], name='Satisfaction'))
            figs['satisfaction'] = fig
        
        return figs

class OperationalDashboard:
    def __init__(self):
        self.real_time_metrics = {}
        self.alerts = []

    def update_real_time_metrics(self, metrics: Dict[str, float]):
        """Update real-time operational metrics"""
        self.real_time_metrics.update({
            'timestamp': datetime.now().isoformat(),
            **metrics
        })

    def check_anomalies(self, data: Dict[str, float]) -> List[Dict[str, Any]]:
        """Check for anomalies in metrics"""
        anomalies = []
        
        # Define thresholds
        thresholds = {
            'order_processing_time': 15,  # minutes
            'inventory_level': 20,  # percentage
            'customer_wait_time': 30  # minutes
        }
        
        for metric, value in data.items():
            if metric in thresholds and value > thresholds[metric]:
                anomalies.append({
                    'metric': metric,
                    'value': value,
                    'threshold': thresholds[metric],
                    'timestamp': datetime.now().isoformat()
                })
        
        self.alerts.extend(anomalies)
        return anomalies

    def create_real_time_charts(self) -> Dict[str, go.Figure]:
        """Create real-time operational charts"""
        charts = {}
        
        # Order processing time
        if 'order_processing_time' in self.real_time_metrics:
            fig = go.Figure()
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=self.real_time_metrics['order_processing_time'],
                title={'text': "Order Processing Time (min)"}
            ))
            charts['processing_time'] = fig
        
        # Inventory levels
        if 'inventory_level' in self.real_time_metrics:
            fig = go.Figure()
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=self.real_time_metrics['inventory_level'],
                title={'text': "Inventory Level (%)"}
            ))
            charts['inventory'] = fig
        
        return charts

class DecisionSupport:
    def __init__(self):
        self.what_if_scenarios = {}
        self.recommendations = []

    def create_what_if_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Create what-if analysis scenario"""
        scenario_id = f"scenario_{len(self.what_if_scenarios)}"
        self.what_if_scenarios[scenario_id] = {
            'timestamp': datetime.now().isoformat(),
            'parameters': scenario,
            'results': self.simulate_scenario(scenario)
        }
        return self.what_if_scenarios[scenario_id]

    def simulate_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate a what-if scenario"""
        # Implement scenario simulation logic
        pass

    def generate_prescriptive_analytics(self, data: Dict[str, Any]) -> List[str]:
        """Generate prescriptive analytics recommendations"""
        recommendations = []
        
        # Analyze revenue optimization
        if 'revenue' in data:
            revenue_recs = self.analyze_revenue_optimization(data['revenue'])
            recommendations.extend(revenue_recs)
        
        # Analyze inventory optimization
        if 'inventory' in data:
            inventory_recs = self.analyze_inventory_optimization(data['inventory'])
            recommendations.extend(inventory_recs)
        
        self.recommendations = recommendations
        return recommendations

    def analyze_revenue_optimization(self, revenue_data: Dict[str, float]) -> List[str]:
        """Analyze revenue optimization opportunities"""
        # Implement revenue optimization analysis
        pass

    def analyze_inventory_optimization(self, inventory_data: Dict[str, float]) -> List[str]:
        """Analyze inventory optimization opportunities"""
        # Implement inventory optimization analysis
        pass

class ReportGeneration:
    def __init__(self):
        self.templates = {}

    def add_template(self, name: str, template_string: str):
        """Add a report template"""
        self.templates[name] = Template(template_string)

    def generate_report(self, template_name: str, data: Dict[str, Any]) -> str:
        """Generate report using template"""
        if template_name not in self.templates:
            raise ValueError(f"Template {template_name} not found")
        
        return self.templates[template_name].render(**data)

class IntegrationPoints:
    def __init__(self):
        self.app = FastAPI()
        
        @self.app.post("/pos/recommendations")
        async def pos_recommendations(data: Dict[str, Any]):
            """Generate POS system recommendations"""
            try:
                return await self.generate_pos_recommendations(data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/inventory/alerts")
        async def inventory_alerts(data: Dict[str, Any]):
            """Generate inventory management alerts"""
            try:
                return await self.generate_inventory_alerts(data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/marketing/suggestions")
        async def marketing_suggestions(data: Dict[str, Any]):
            """Generate marketing campaign suggestions"""
            try:
                return await self.generate_marketing_suggestions(data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    async def generate_pos_recommendations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate POS system recommendations"""
        # Implement POS recommendations
        pass

    async def generate_inventory_alerts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate inventory management alerts"""
        # Implement inventory alerts
        pass

    async def generate_marketing_suggestions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate marketing campaign suggestions"""
        # Implement marketing suggestions
        pass

async def fetch_metrics(session: aiohttp.ClientSession, endpoint: str) -> Dict[str, Any]:
    """Fetch metrics from backend API"""
    try:
        async with session.get(f"{config.BACKEND_API_URL}/{endpoint}") as response:
            if response.status == 200:
                return await response.json()
            else:
                st.error(f"Error fetching {endpoint}: {response.status}")
                return {}
    except Exception as e:
        st.error(f"Failed to fetch {endpoint}: {str(e)}")
        return {}

async def fetch_recommendations(session: aiohttp.ClientSession) -> List[str]:
    """Fetch AI-generated recommendations"""
    try:
        async with session.get(f"{config.AI_AGENT_URL}/recommendations") as response:
            if response.status == 200:
                data = await response.json()
                return data.get('recommendations', [])
            else:
                st.error(f"Error fetching recommendations: {response.status}")
                return []
    except Exception as e:
        st.error(f"Failed to fetch recommendations: {str(e)}")
        return []

def create_streamlit_dashboard():
    """Create Streamlit dashboard"""
    st.title("Restaurant BI Dashboard")
    
    # Sidebar with error handling for date input
    st.sidebar.title("Controls")
    try:
        date_range = st.sidebar.date_input("Select Date Range", [])
    except Exception as e:
        st.sidebar.error(f"Error with date input: {str(e)}")
        date_range = []
    
    # Create async session and fetch data
    async def fetch_dashboard_data():
        async with aiohttp.ClientSession() as session:
            # Fetch metrics concurrently
            exec_metrics, op_metrics, recommendations = await asyncio.gather(
                fetch_metrics(session, "executive_metrics"),
                fetch_metrics(session, "operational_metrics"),
                fetch_recommendations(session)
            )
            
            # Executive metrics with error handling
            st.header("Executive Metrics")
            col1, col2, col3 = st.columns(3)
            with col1:
                revenue = exec_metrics.get('revenue', {'value': 0, 'change': '0%'})
                st.metric("Revenue", f"${revenue['value']:,.2f}", revenue['change'])
            with col2:
                satisfaction = exec_metrics.get('satisfaction', {'value': 0, 'change': '0'})
                st.metric("Customer Satisfaction", f"{satisfaction['value']}/5", satisfaction['change'])
            with col3:
                market = exec_metrics.get('market_share', {'value': 0, 'change': '0%'})
                st.metric("Market Share", f"{market['value']}%", market['change'])
            
            # Operational metrics with error handling
            st.header("Operational Metrics")
            col1, col2 = st.columns(2)
            with col1:
                proc_time = op_metrics.get('processing_time', {'value': 0, 'change': '0'})
                st.metric("Order Processing Time", f"{proc_time['value']} min", proc_time['change'])
            with col2:
                inventory = op_metrics.get('inventory', {'value': 0, 'change': '0%'})
                st.metric("Inventory Level", f"{inventory['value']}%", inventory['change'])
            
            # AI-generated recommendations
            st.header("Recommendations")
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    st.write(f"{i}. {rec}")
            else:
                st.info("No recommendations available at the moment")

    # Run async data fetching
    try:
        asyncio.run(fetch_dashboard_data())
    except Exception as e:
        st.error(f"Failed to load dashboard data: {str(e)}")

if __name__ == "__main__":
    create_streamlit_dashboard()
