import asyncio
import os
from typing import Dict, Any
from restack_ai import Restack
from datetime import datetime
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

class RestaurantBIService:
    def __init__(self):
        self.client = Restack()

    async def initialize_service(self):
        """Initialize and start the Restack service"""
        print("Initializing Restaurant BI Service...")
        
        # Register workflows and functions
        await self.client.start_service(
            name="restaurant_bi",
            description="Restaurant Business Intelligence System",
            workflows=[
                {
                    "name": "market_analysis",
                    "description": "Analyze market trends and patterns",
                    "handler": analyze_market_trends
                },
                {
                    "name": "competitor_analysis",
                    "description": "Analyze competitor data and strategies",
                    "handler": analyze_competitor_data
                }
            ],
            functions=[
                collect_pos_data,
                collect_inventory_data,
                generate_executive_insights,
                generate_operational_metrics
            ]
        )

    async def schedule_recurring_tasks(self):
        """Schedule recurring tasks in Restack"""
        # Daily data collection
        await self.client.schedule_workflow(
            workflow_name="data_collection",
            cron="0 0 * * *",  # Daily at midnight
            input={
                "type": "daily_collection",
                "sources": ["pos", "inventory"]
            }
        )

        # Weekly market analysis
        await self.client.schedule_workflow(
            workflow_name="market_analysis",
            cron="0 0 * * 0",  # Weekly on Sunday
            input={
                "type": "market_analysis",
                "include_competitors": True
            }
        )

        # Hourly metrics update
        await self.client.schedule_workflow(
            workflow_name="bi_analysis",
            cron="0 * * * *",  # Every hour
            input={
                "type": "metrics_update",
                "metrics": ["sales", "inventory", "customer_satisfaction"]
            }
        )

    async def register_event_handlers(self):
        """Register event handlers for real-time updates"""
        await self.client.register_event_handler(
            event_type="pos_update",
            handler=self.handle_pos_update
        )

        await self.client.register_event_handler(
            event_type="inventory_update",
            handler=self.handle_inventory_update
        )

        await self.client.register_event_handler(
            event_type="customer_feedback",
            handler=self.handle_customer_feedback
        )

    async def handle_pos_update(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle real-time POS updates"""
        try:
            # Process POS data
            processed_data = await collect_pos_data(event_data)
            
            # Generate updated insights
            insights = await generate_executive_insights({
                "data_type": "pos",
                "data": processed_data
            })
            
            return {
                "status": "success",
                "processed_data": processed_data,
                "insights": insights
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    async def handle_inventory_update(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle real-time inventory updates"""
        try:
            # Process inventory data
            processed_data = await collect_inventory_data(event_data)
            
            # Generate updated metrics
            metrics = await generate_operational_metrics({
                "data_type": "inventory",
                "data": processed_data
            })
            
            return {
                "status": "success",
                "processed_data": processed_data,
                "metrics": metrics
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    async def handle_customer_feedback(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle real-time customer feedback"""
        try:
            # Analyze feedback
            analysis_result = await analyze_market_trends({
                "data_type": "customer_feedback",
                "data": event_data
            })
            
            return {
                "status": "success",
                "analysis": analysis_result
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

async def main():
    """Main entry point for the service"""
    service = RestaurantBIService()
    
    # Initialize service
    await service.initialize_service()
    
    # Register event handlers
    await service.register_event_handlers()
    
    # Schedule recurring tasks
    await service.schedule_recurring_tasks()
    
    print("Restaurant BI Service is running...")
    
    # Keep the service running
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())