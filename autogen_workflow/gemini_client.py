"""
Custom Gemini Client for AutoGen Integration

This module provides a wrapper to use Google Gemini API with AutoGen framework
using the official REST API as documented at:
https://ai.google.dev/api/rest/v1beta/models/generateContent
"""

import asyncio
import logging
import json
import aiohttp
from typing import List, Dict, Any, Optional, AsyncGenerator, Union
from autogen_core.models import ChatCompletionClient
from autogen_core.models._types import (
    CreateResult,
    LLMMessage,
    SystemMessage,
    UserMessage,
    AssistantMessage,
    FunctionExecutionResultMessage
)


class GeminiChatCompletionClient(ChatCompletionClient):
    """
    Custom Gemini Chat Completion Client for AutoGen.

    This client uses Google's Gemini REST API to work with AutoGen's ChatCompletionClient interface.
    Based on: https://ai.google.dev/api/rest/v1beta/models/generateContent
    """

    def __init__(
        self,
        model: str = "gemini-2.0-flash",
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        **kwargs
    ):
        """
        Initialize the Gemini client.

        Args:
            model: Gemini model name
            api_key: Google API key
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
        """
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Gemini API endpoint
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

        self.logger = logging.getLogger(__name__)

        if not api_key:
            raise ValueError("Google API key is required for Gemini client")
        
    async def create(
        self,
        messages: List[LLMMessage],
        *,
        cancellation_token: Optional[Any] = None,
        **kwargs
    ) -> CreateResult:
        """
        Create a chat completion using Gemini API.
        
        Args:
            messages: List of messages in the conversation
            cancellation_token: Cancellation token (not used)
            **kwargs: Additional parameters
            
        Returns:
            CreateResult with the completion
        """
        try:
            # Convert AutoGen messages to Gemini format
            payload = self._convert_messages(messages)

            # Generate response using Gemini
            response = await self._generate_response(payload)

            # Convert response back to AutoGen format
            return self._create_result(response, messages)
            
        except Exception as e:
            self.logger.error(f"Error in Gemini API call: {str(e)}")
            raise
    
    def _convert_messages(self, messages: List[LLMMessage]) -> Dict[str, Any]:
        """Convert AutoGen messages to Gemini API format with system instruction support."""

        system_instruction = None
        gemini_contents = []

        # Separate system messages from other messages
        for message in messages:
            if isinstance(message, SystemMessage):
                if not system_instruction:
                    system_instruction = {
                        "parts": [{"text": str(message.content)}]
                    }
            elif isinstance(message, UserMessage):
                gemini_contents.append({
                    "parts": [{"text": str(message.content)}]
                })
            elif isinstance(message, AssistantMessage):
                # For conversation history, we might want to include assistant messages
                # but for now, we'll focus on the latest user message
                pass
            elif isinstance(message, FunctionExecutionResultMessage):
                gemini_contents.append({
                    "parts": [{"text": f"Function result: {message.content}"}]
                })

        # If no user messages, create a default one
        if not gemini_contents:
            gemini_contents.append({
                "parts": [{"text": "Hello"}]
            })

        # Prepare the full request payload
        payload = {
            "contents": gemini_contents,
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens
            }
        }

        # Add system instruction if available (required for preview models)
        if system_instruction:
            payload["systemInstruction"] = system_instruction
        elif "preview" in self.model.lower():
            # Add default system instruction for preview models
            payload["systemInstruction"] = {
                "parts": [{"text": "You are a helpful AI assistant. Provide clear, direct responses."}]
            }

        return payload
    
    async def _generate_response(self, payload: Dict[str, Any]) -> str:
        """Generate response using Gemini REST API."""
        try:
            # The payload is already prepared by _convert_messages

            # API endpoint
            url = f"{self.base_url}/models/{self.model}:generateContent"

            # Headers
            headers = {
                "Content-Type": "application/json"
            }

            # Parameters
            params = {
                "key": self.api_key
            }

            # Make the API call with timeout
            timeout = aiohttp.ClientTimeout(total=30)  # 30 second timeout
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    url,
                    json=payload,
                    headers=headers,
                    params=params
                ) as response:

                    if response.status == 200:
                        result = await response.json()

                        # Extract the generated text
                        if "candidates" in result and len(result["candidates"]) > 0:
                            candidate = result["candidates"][0]
                            if "content" in candidate and "parts" in candidate["content"]:
                                parts = candidate["content"]["parts"]
                                if len(parts) > 0 and "text" in parts[0]:
                                    return parts[0]["text"]

                        return "I apologize, but I couldn't generate a response."

                    else:
                        error_text = await response.text()
                        self.logger.error(f"Gemini API error {response.status}: {error_text}")
                        return f"API Error {response.status}: {error_text}"

        except Exception as e:
            self.logger.error(f"Error generating Gemini response: {str(e)}")
            return f"Error: {str(e)}"
    
    def _create_result(self, response_text: str, original_messages: List[LLMMessage]) -> CreateResult:
        """Create AutoGen CreateResult from Gemini response."""

        # Import RequestUsage for proper usage tracking
        from autogen_core.models._types import RequestUsage

        # Create usage info (estimated)
        usage = RequestUsage(
            prompt_tokens=sum(len(str(msg.content).split()) for msg in original_messages if hasattr(msg, 'content')),
            completion_tokens=len(response_text.split()),
        )

        # Create a proper result structure
        result = CreateResult(
            content=response_text,
            finish_reason="stop",
            usage=usage,
            cached=False  # Required field
        )

        return result
    
    async def create_stream(
        self,
        messages: List[LLMMessage],
        *,
        cancellation_token: Optional[Any] = None,
        **kwargs
    ) -> AsyncGenerator[Union[str, CreateResult], None]:
        """
        Create a streaming chat completion.
        
        For now, this just yields the complete result.
        A full implementation would stream tokens as they're generated.
        """
        result = await self.create(messages, cancellation_token=cancellation_token, **kwargs)
        yield result
    
    @property
    def capabilities(self) -> Dict[str, Any]:
        """Return client capabilities."""
        return {
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "streaming": True
        }
    
    def count_tokens(self, messages: List[LLMMessage]) -> int:
        """Count tokens in messages (rough estimate)."""
        total = 0
        for message in messages:
            if hasattr(message, 'content') and message.content:
                total += len(str(message.content).split())
        return total
    
    def remaining_tokens(self, messages: List[LLMMessage]) -> int:
        """Calculate remaining tokens."""
        used = self.count_tokens(messages)
        return max(0, self.max_tokens - used)

    # Required abstract methods from ChatCompletionClient

    async def actual_usage(self) -> Any:
        """Return actual usage statistics."""
        return None

    async def close(self) -> None:
        """Close the client connection."""
        pass

    @property
    def model_info(self) -> Dict[str, Any]:
        """Return model information."""
        return {
            "model": self.model,
            "provider": "google",
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "function_calling": True,  # Enable function calling for handoffs
            "vision": False,
            "json_output": True
        }

    def total_usage(self) -> Any:
        """Return total usage statistics."""
        return None
