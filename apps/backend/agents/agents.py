"""
Chat RAG (Retrieval Augmented Generation) Agent Module

This module implements a chat agent that uses RAG to enhance responses with sales data.
"""

from datetime import timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from restack_ai.agent import agent, import_functions, log
from restack_ai.agent.exceptions import (
    AgentError,
    AgentTimeoutError,
    AgentValidationError,
)
from restack_ai.agent.retry import retry

# Configuration constants
MAX_MESSAGE_HISTORY = 50
MAX_RETRIES = 3
RETRY_DELAY = 1.0  # seconds
SALES_LOOKUP_TIMEOUT = timedelta(seconds=120)
CHAT_COMPLETION_TIMEOUT = timedelta(seconds=120)
SYSTEM_PROMPT = """You are a helpful assistant that can help with sales data.
Current sales information: {sales_info}
Please provide accurate and relevant responses based on this data."""

# Import functions directly from functions.py
with import_functions():
    from apps.backend.functions import (
        llm_chat,
        Message,
        LlmChatResponse,
        lookupSales,
        SalesData,
    )

class AgentRagError(AgentError):
    """Base exception for AgentRag errors."""
    pass

class MessageProcessingError(AgentRagError):
    """Exception raised when message processing fails."""
    pass

class SalesLookupError(AgentRagError):
    """Exception raised when sales data lookup fails."""
    pass

class MessageEvent(BaseModel):
    """Event model for incoming chat messages."""
    content: str = Field(..., min_length=1)

    @validator("content")
    def validate_content(cls, v: str) -> str:
        """Validate message content is not just whitespace."""
        if v.strip() == "":
            raise ValueError("Message content cannot be empty or whitespace")
        return v

class EndEvent(BaseModel):
    """Event model for ending the chat session."""
    end: bool = Field(...)

class AgentInput(BaseModel):
    """Input model for agent initialization."""
    max_history: Optional[int] = Field(default=MAX_MESSAGE_HISTORY)
    system_prompt: Optional[str] = Field(default=SYSTEM_PROMPT)

@agent.defn()
class AgentRag:
    """
    A RAG-enabled chat agent that enhances responses with relevant sales data.
    
    This agent handles message events by:
    1. Looking up relevant sales data
    2. Maintaining conversation history
    3. Generating contextual responses using an LLM
    """
    
    def __init__(self) -> None:
        """Initialize the agent with empty message history."""
        self.end: bool = False
        self.messages: List[Message] = []
        self._sales_cache: Optional[SalesData] = None
        self._max_history: int = MAX_MESSAGE_HISTORY
        self._system_prompt: str = SYSTEM_PROMPT

    @retry(
        retries=MAX_RETRIES,
        delay=RETRY_DELAY,
        exceptions=(AgentTimeoutError, SalesLookupError)
    )
    async def _get_sales_info(self) -> SalesData:
        """
        Retrieve sales information with caching and retry logic.
        
        Returns:
            SalesData: Sales information
        
        Raises:
            SalesLookupError: If sales lookup fails after retries
        """
        if not self._sales_cache:
            try:
                self._sales_cache = await agent.step(
                    lookupSales,
                    start_to_close_timeout=SALES_LOOKUP_TIMEOUT
                )
            except AgentError as e:
                log.error(f"Failed to lookup sales data: {str(e)}")
                raise SalesLookupError("Unable to retrieve sales information") from e
            except Exception as e:
                log.error(f"Unexpected error in sales lookup: {str(e)}")
                raise SalesLookupError("Unexpected error during sales lookup") from e

        return self._sales_cache

    def _trim_message_history(self) -> None:
        """Maintain message history within configured size limits."""
        while len(self.messages) > self._max_history:
            self.messages.pop(0)

    @retry(
        retries=MAX_RETRIES,
        delay=RETRY_DELAY,
        exceptions=(AgentTimeoutError, MessageProcessingError)
    )
    async def _generate_completion(
        self, system_content: str
    ) -> LlmChatResponse:
        """
        Generate chat completion with retry logic.
        
        Args:
            system_content: System context for the LLM
            
        Returns:
            LlmChatResponse: Generated completion
            
        Raises:
            MessageProcessingError: If completion generation fails
        """
        try:
            completion = await agent.step(
                llm_chat,
                self.messages,
                system_content,
                start_to_close_timeout=CHAT_COMPLETION_TIMEOUT,
            )
            
            if not completion or not completion.choices:
                raise MessageProcessingError("Invalid completion response")
                
            return completion
            
        except AgentError as e:
            log.error(f"Chat completion failed: {str(e)}")
            raise MessageProcessingError("Failed to generate response") from e
        except Exception as e:
            log.error(f"Unexpected error in completion: {str(e)}")
            raise MessageProcessingError("Unexpected error generating response") from e

    @agent.event
    async def message(self, message: MessageEvent) -> List[Message]:
        """
        Handle incoming chat messages.
        
        Args:
            message: The incoming message event
            
        Returns:
            List[Message]: Updated message history
            
        Raises:
            MessageProcessingError: If message processing fails
        """
        try:
            log.info(f"Processing message: {message.content}")

            # Get sales context
            sales_info = await self._get_sales_info()
            system_content = self._system_prompt.format(sales_info=sales_info)

            # Add user message
            self.messages.append(Message(role="user", content=message.content))
            self._trim_message_history()

            # Generate and process completion
            completion = await self._generate_completion(system_content)
            assistant_message = completion.choices[0].message.content
            
            log.info(f"Generated response: {assistant_message}")

            # Add assistant response
            self.messages.append(
                Message(role="assistant", content=assistant_message or "")
            )

            return self.messages

        except (SalesLookupError, MessageProcessingError) as e:
            log.error(f"Error in message handler: {str(e)}")
            raise
        except Exception as e:
            log.error(f"Unexpected error in message handler: {str(e)}")
            raise MessageProcessingError(f"Chat processing error: {str(e)}") from e

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        """
        Handle chat end event.
        
        Args:
            end: The end event
            
        Returns:
            EndEvent: Confirmation of end status
        """
        log.info("Ending chat session")
        self.end = True
        return EndEvent(end=True)

    @agent.run
    async def run(self, input: Optional[Dict[str, Any]] = None) -> None:
        """
        Main agent run loop.
        
        Args:
            input: Optional configuration parameters
                max_history: Maximum number of messages to keep
                system_prompt: Custom system prompt template
        """
        try:
            # Validate and process input
            if input:
                validated_input = AgentInput(**input)
                self._max_history = validated_input.max_history
                if validated_input.system_prompt:
                    self._system_prompt = validated_input.system_prompt

            log.info(
                f"Starting chat agent (max_history={self._max_history})"
            )
            
            await agent.condition(lambda: self.end)
            
        except AgentValidationError as e:
            log.error(f"Input validation error: {str(e)}")
            raise
        except Exception as e:
            log.error(f"Error in agent run loop: {str(e)}")
            raise AgentRagError("Failed to run chat agent") from e
