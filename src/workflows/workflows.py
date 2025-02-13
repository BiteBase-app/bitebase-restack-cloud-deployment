from typing import Dict, Any
from abacusai.api_class import *
from src.functions.market_analysis import (
    analyze_market_trends,
    analyze_competitor_data,
    analyze_customer_sentiment,
    analyze_menu_performance
)
from src.functions.data_collection import (
    collect_pos_data,
    collect_inventory_data,
    collect_customer_feedback,
    collect_external_data
)
from src.functions.bi_analytics import (
    generate_executive_insights,
    generate_operational_metrics,
    generate_recommendations
)

def create_market_analysis_workflow() -> WorkflowGraph:
    """Create market analysis workflow"""
    # Data Collection Node
    data_collection = WorkflowGraphNode(
        name="DataCollection",
        function=collect_external_data,
        input_mappings=[
            WorkflowNodeInputMapping(
                name="location",
                variable_type=WorkflowNodeInputType.DICT,
                is_required=True
            )
        ],
        output_mappings=[
            WorkflowNodeOutputMapping(
                name="market_data",
                variable_type=WorkflowNodeOutputType.DICT
            )
        ]
    )

    # Market Analysis Node
    market_analysis = WorkflowGraphNode(
        name="MarketAnalysis",
        function=analyze_market_trends,
        input_mappings=[
            WorkflowNodeInputMapping(
                name="data",
                variable_type=WorkflowNodeInputType.DICT,
                is_required=True
            )
        ],
        output_mappings=[
            WorkflowNodeOutputMapping(
                name="analysis_results",
                variable_type=WorkflowNodeOutputType.DICT
            )
        ]
    )

    return WorkflowGraph(
        nodes=[data_collection, market_analysis],
        specification_type='execution_flow'
    )

def create_data_collection_workflow() -> WorkflowGraph:
    """Create data collection workflow"""
    # POS Data Collection
    pos_node = WorkflowGraphNode(
        name="POSDataCollection",
        function=collect_pos_data,
        input_mappings=[
            WorkflowNodeInputMapping(
                name="start_date",
                variable_type=WorkflowNodeInputType.STRING,
                is_required=True
            ),
            WorkflowNodeInputMapping(
                name="end_date",
                variable_type=WorkflowNodeInputType.STRING,
                is_required=True
            )
        ],
        output_mappings=[
            WorkflowNodeOutputMapping(
                name="pos_data",
                variable_type=WorkflowNodeOutputType.DICT
            )
        ]
    )

    # Inventory Data Collection
    inventory_node = WorkflowGraphNode(
        name="InventoryDataCollection",
        function=collect_inventory_data,
        output_mappings=[
            WorkflowNodeOutputMapping(
                name="inventory_data",
                variable_type=WorkflowNodeOutputType.DICT
            )
        ]
    )

    # Customer Feedback Collection
    feedback_node = WorkflowGraphNode(
        name="FeedbackCollection",
        function=collect_customer_feedback,
        output_mappings=[
            WorkflowNodeOutputMapping(
                name="feedback_data",
                variable_type=WorkflowNodeOutputType.DICT
            )
        ]
    )

    return WorkflowGraph(
        nodes=[pos_node, inventory_node, feedback_node],
        specification_type='execution_flow'
    )

def create_bi_analysis_workflow() -> WorkflowGraph:
    """Create business intelligence analysis workflow"""
    # Executive Insights Node
    executive_node = WorkflowGraphNode(
        name="ExecutiveInsights",
        function=generate_executive_insights,
        input_mappings=[
            WorkflowNodeInputMapping(
                name="data",
                variable_type=WorkflowNodeInputType.DICT,
                is_required=True
            )
        ],
        output_mappings=[
            WorkflowNodeOutputMapping(
                name="executive_insights",
                variable_type=WorkflowNodeOutputType.DICT
            )
        ]
    )

    # Operational Metrics Node
    operational_node = WorkflowGraphNode(
        name="OperationalMetrics",
        function=generate_operational_metrics,
        input_mappings=[
            WorkflowNodeInputMapping(
                name="data",
                variable_type=WorkflowNodeInputType.DICT,
                is_required=True
            )
        ],
        output_mappings=[
            WorkflowNodeOutputMapping(
                name="operational_metrics",
                variable_type=WorkflowNodeOutputType.DICT
            )
        ]
    )

    # Recommendations Node
    recommendations_node = WorkflowGraphNode(
        name="Recommendations",
        function=generate_recommendations,
        input_mappings=[
            WorkflowNodeInputMapping(
                name="analysis",
                variable_type=WorkflowNodeInputType.DICT,
                is_required=True
            )
        ],
        output_mappings=[
            WorkflowNodeOutputMapping(
                name="recommendations",
                variable_type=WorkflowNodeOutputType.LIST
            )
        ]
    )

    return WorkflowGraph(
        nodes=[executive_node, operational_node, recommendations_node],
        specification_type='execution_flow'
    )