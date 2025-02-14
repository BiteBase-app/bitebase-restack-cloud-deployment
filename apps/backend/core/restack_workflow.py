import asyncio
from typing import Dict, Any
from restack_ai import Restack
from src.functions.market_analysis import (
    analyze_market_trends,
    analyze_competitor_data
)
from src.functions.data_collection import (
    collect_pos_data,
    collect_inventory_data
)
from src.functions.bi_analytics import (
    generate_executive_insights,
    generate_operational_metrics
)

# Initialize Restack client
client = Restack()

# Workflow Events
async def on_market_analysis(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle market analysis event"""
    return await analyze_market_trends(event_data)

async def on_competitor_analysis(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle competitor analysis event"""
    return await analyze_competitor_data(event_data)

async def on_data_collection(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle data collection event"""
    pos_data = await collect_pos_data(event_data)
    inventory_data = await collect_inventory_data(event_data)
    return {
        "pos_data": pos_data,
        "inventory_data": inventory_data
    }

async def on_bi_analysis(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle business intelligence analysis event"""
    insights = await generate_executive_insights(event_data)
    metrics = await generate_operational_metrics(event_data)
    return {
        "insights": insights,
        "metrics": metrics
    }

# Register workflow events with Restack
async def register_workflows():
    """Register workflows with Restack"""
    await client.register_event_handler(
        "market_analysis",
        on_market_analysis,
        description="Analyze market trends and patterns"
    )

    await client.register_event_handler(
        "competitor_analysis",
        on_competitor_analysis,
        description="Analyze competitor data and strategies"
    )

    await client.register_event_handler(
        "data_collection",
        on_data_collection,
        description="Collect POS and inventory data"
    )

    await client.register_event_handler(
        "bi_analysis",
        on_bi_analysis,
        description="Generate business intelligence insights"
    )

if __name__ == "__main__":
    # Run workflow registration
    asyncio.run(register_workflows())