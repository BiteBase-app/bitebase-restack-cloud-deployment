"""
Backend Functions Module

This module provides core functionality for the backend services.
"""

import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
from restack_ai.function import function, FunctionFailure, log
from apps.backend.core.connections import (
    get_db_engine,
    get_redis_client,
    get_ai_agent_client,
)

# Initialize service connections
db_engine = get_db_engine()
redis_client = get_redis_client()

@dataclass
class Message:
    """Message class for chat conversations."""
    role: str
    content: str

@dataclass
class ChatChoice:
    """Represents a single chat completion choice."""
    message: Message
    finish_reason: Optional[str] = None
    index: int = 0

@dataclass
class LlmChatResponse:
    """Response model for LLM chat function."""
    choices: List[ChatChoice]
    model: Optional[str] = None
    created: Optional[int] = None

@dataclass
class SalesData:
    """Container for sales data results."""
    data: Dict[str, Any]
    source: str  # 'cache' or 'database'
    timestamp: str

def _sanitize_input(query: str) -> str:
    """
    Sanitize the input query to prevent SQL injection.
    
    Args:
        query: Raw query string
        
    Returns:
        str: Sanitized query string
    """
    return query.replace("'", "''")

@function.defn()
async def lookupSales(query: Optional[str] = None) -> SalesData:
    """
    Look up sales data in the database with caching.
    
    Args:
        query: Optional search query to filter sales data
        
    Returns:
        SalesData: Retrieved sales information
        
    Raises:
        FunctionFailure: If lookup fails
    """
    cache_key = f"sales_lookup_{query}" if query else "sales_lookup_all"
    
    try:
        # Try cache first
        if cached_data := redis_client.get(cache_key):
            log.info("Cache hit for sales data", query=query)
            return SalesData(
                data=json.loads(cached_data.decode('utf-8')),
                source="cache",
                timestamp=redis_client.get(f"{cache_key}_timestamp").decode('utf-8')
            )
    except Exception as e:
        log.warning("Cache retrieval failed", error=str(e))
    
    try:
        # Construct query
        base_query = "SELECT * FROM sales"
        if query:
            sanitized_query = _sanitize_input(query)
            where_clause = f" WHERE data LIKE '%{sanitized_query}%'"
            full_query = base_query + where_clause
        else:
            full_query = base_query

        # Execute query
        with db_engine.connect() as conn:
            result = conn.execute(full_query).fetchall()
            data = [dict(row) for row in result]
            
            # Cache the results
            try:
                timestamp = datetime.now().isoformat()
                redis_client.setex(
                    cache_key,
                    3600,  # 1 hour expiration
                    json.dumps(data)
                )
                redis_client.setex(
                    f"{cache_key}_timestamp",
                    3600,
                    timestamp
                )
            except Exception as e:
                log.warning("Failed to cache results", error=str(e))
            
            return SalesData(
                data=data,
                source="database",
                timestamp=datetime.now().isoformat()
            )
            
    except Exception as e:
        log.error("Database lookup failed", error=str(e))
        raise FunctionFailure(f"Failed to retrieve sales data: {str(e)}") from e

@function.defn()
async def llm_chat(messages: List[Message], system_content: str) -> LlmChatResponse:
    """
    Process chat with AI agent.
    
    Args:
        messages: List of conversation messages
        system_content: System context for the LLM
        
    Returns:
        LlmChatResponse: Chat completion response
        
    Raises:
        FunctionFailure: If chat processing fails
    """
    log.info("Processing chat", num_messages=len(messages))
    
    try:
        async with aiohttp.ClientSession() as session:
            session, ai_url = await get_ai_agent_client(session)
            
            payload = {
                "messages": [
                    {"role": msg.role, "content": msg.content}
                    for msg in messages
                ],
                "system_content": system_content
            }
            
            async with session.post(f"{ai_url}/chat", json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise FunctionFailure(
                        f"AI agent error {response.status}: {error_text}"
                    )
                    
                result = await response.json()
                
                if not result or "choices" not in result:
                    raise FunctionFailure("Invalid response format from AI agent")
                
                choices = [
                    ChatChoice(
                        message=Message(
                            role=choice["message"]["role"],
                            content=choice["message"]["content"]
                        ),
                        finish_reason=choice.get("finish_reason"),
                        index=choice.get("index", 0)
                    )
                    for choice in result["choices"]
                ]
                
                return LlmChatResponse(
                    choices=choices,
                    model=result.get("model"),
                    created=result.get("created")
                )
                
    except Exception as e:
        log.error("Chat processing failed", error=str(e))
        raise FunctionFailure(f"Failed to process chat: {str(e)}") from e
