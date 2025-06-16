"""
Mock Gemini Client for AutoGen Integration

This is a temporary mock client to test the AutoGen workflow
while we resolve the network connectivity issues.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator, Union
from autogen_core.models import ChatCompletionClient
from autogen_core.models._types import (
    CreateResult,
    LLMMessage,
    SystemMessage,
    UserMessage,
    AssistantMessage,
    FunctionExecutionResultMessage,
    RequestUsage
)


class MockGeminiChatCompletionClient(ChatCompletionClient):
    """
    Mock Gemini Chat Completion Client for AutoGen.
    
    This client simulates Gemini responses for testing purposes.
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
        Initialize the mock Gemini client.
        
        Args:
            model: Gemini model name
            api_key: Google API key (not used in mock)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
        """
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized Mock Gemini client with model: {model}")
        
    async def create(
        self,
        messages: List[LLMMessage],
        *,
        cancellation_token: Optional[Any] = None,
        **kwargs
    ) -> CreateResult:
        """
        Create a mock chat completion.
        
        Args:
            messages: List of messages in the conversation
            cancellation_token: Cancellation token (not used)
            **kwargs: Additional parameters
            
        Returns:
            CreateResult with the mock completion
        """
        try:
            # Extract the last user message for context
            last_message = ""
            for message in reversed(messages):
                if isinstance(message, (UserMessage, SystemMessage)):
                    last_message = str(message.content)
                    break
            
            # Generate a mock response based on the message content
            response = self._generate_mock_response(last_message)
            
            # Create result
            return self._create_result(response, messages)
            
        except Exception as e:
            self.logger.error(f"Error in mock Gemini API call: {str(e)}")
            raise
    
    def _generate_mock_response(self, message: str) -> str:
        """Generate a mock response based on the input message."""
        
        message_lower = message.lower()
        
        # Architecture-related responses
        if "architect" in message_lower or "design" in message_lower or "architecture" in message_lower:
            return """# System Architecture Design

## Overview
I'll design a simple FastAPI application with the following architecture:

## Components
1. **Main Application** (`main.py`)
   - FastAPI app instance
   - Route definitions
   - Error handling middleware

2. **Health Check Endpoint** (`/health`)
   - Simple status check
   - Returns JSON response

3. **Calculator Endpoint** (`/calculate`)
   - POST endpoint for number addition
   - Input validation using Pydantic models
   - Error handling for invalid inputs

## Technical Stack
- **Framework**: FastAPI
- **Validation**: Pydantic models
- **Logging**: Python logging module
- **Testing**: pytest

## File Structure
```
fastapi_app/
├── main.py          # Main application
├── models.py        # Pydantic models
├── test_main.py     # Tests
└── requirements.txt # Dependencies
```

This architecture ensures separation of concerns and maintainability.
"""

        # Project management responses
        elif "project" in message_lower or "plan" in message_lower or "manager" in message_lower:
            return """# Implementation Plan

## Phase 1: Project Setup
- [ ] Create project structure
- [ ] Set up virtual environment
- [ ] Install FastAPI dependencies

## Phase 2: Core Implementation
- [ ] Implement main FastAPI application
- [ ] Create Pydantic models for validation
- [ ] Implement health check endpoint
- [ ] Implement calculator endpoint

## Phase 3: Error Handling & Logging
- [ ] Add comprehensive error handling
- [ ] Implement logging system
- [ ] Add input validation

## Phase 4: Testing
- [ ] Write unit tests
- [ ] Test all endpoints
- [ ] Validate error scenarios

## Timeline
- Phase 1: 30 minutes
- Phase 2: 1 hour
- Phase 3: 30 minutes
- Phase 4: 45 minutes

Total estimated time: 2.75 hours
"""

        # Programming responses
        elif "code" in message_lower or "implement" in message_lower or "programmer" in message_lower:
            return """# FastAPI Implementation

Here's the complete implementation:

## main.py
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Simple Calculator API", version="1.0.0")

class CalculationRequest(BaseModel):
    a: float
    b: float

class CalculationResponse(BaseModel):
    result: float
    operation: str

@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "healthy"}

@app.post("/calculate", response_model=CalculationResponse)
async def calculate(request: CalculationRequest):
    try:
        logger.info(f"Calculation requested: {request.a} + {request.b}")
        result = request.a + request.b
        return CalculationResponse(result=result, operation="addition")
    except Exception as e:
        logger.error(f"Calculation error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid calculation")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## test_main.py
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_calculate():
    response = client.post("/calculate", json={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 5
```
"""

        # Code review responses
        elif "review" in message_lower or "quality" in message_lower:
            return """# Code Review Report

## Overall Assessment: ✅ GOOD

## Strengths
1. **Clean Structure**: Well-organized code with clear separation
2. **Type Hints**: Proper use of Pydantic models for validation
3. **Error Handling**: Appropriate HTTP exceptions
4. **Logging**: Good logging implementation
5. **Testing**: Basic test coverage included

## Recommendations
1. **Add more comprehensive tests** for edge cases
2. **Consider rate limiting** for production use
3. **Add API documentation** with more detailed descriptions
4. **Implement request/response logging middleware**

## Security Considerations
- Input validation is properly handled by Pydantic
- No obvious security vulnerabilities
- Consider adding CORS middleware if needed

## Performance Notes
- Simple operations, no performance concerns
- Consider async database operations for future enhancements

## Code Quality Score: 8.5/10
"""

        # Optimization responses
        elif "optim" in message_lower or "performance" in message_lower:
            return """# Code Optimization Report

## Performance Optimizations Applied

### 1. Async/Await Optimization
- All endpoints are properly async
- Non-blocking operations where possible

### 2. Response Model Optimization
```python
# Optimized response models
class OptimizedCalculationResponse(BaseModel):
    result: float
    operation: str
    timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

### 3. Logging Optimization
- Structured logging with correlation IDs
- Async logging for better performance

### 4. Memory Optimization
- Minimal object creation
- Efficient data structures

## Benchmarks
- Health endpoint: ~0.5ms response time
- Calculate endpoint: ~1.2ms response time
- Memory usage: ~15MB baseline

## Production Recommendations
1. Use gunicorn with multiple workers
2. Implement connection pooling
3. Add caching for frequent calculations
4. Use async logging handlers

## Optimization Score: 9/10
The code is well-optimized for its scope and requirements.
"""

        # Default response
        else:
            return f"""Thank you for your message. As a Gemini AI assistant, I'm here to help with your programming workflow.

Your message: "{message[:100]}{'...' if len(message) > 100 else ''}"

I can assist with:
- System architecture design
- Project planning and management  
- Code implementation
- Code review and quality assessment
- Performance optimization

Please let me know how I can help with your specific task!"""
    
    def _create_result(self, response_text: str, original_messages: List[LLMMessage]) -> CreateResult:
        """Create AutoGen CreateResult from mock response."""
        
        # Create usage info (estimated)
        usage = RequestUsage(
            prompt_tokens=sum(len(str(msg.content).split()) for msg in original_messages if hasattr(msg, 'content')),
            completion_tokens=len(response_text.split()),
        )
        
        # Create result
        result = CreateResult(
            content=response_text,
            finish_reason="stop",
            usage=usage,
            cached=False
        )
        
        return result
    
    async def create_stream(
        self,
        messages: List[LLMMessage],
        *,
        cancellation_token: Optional[Any] = None,
        **kwargs
    ) -> AsyncGenerator[Union[str, CreateResult], None]:
        """Create a streaming mock completion."""
        result = await self.create(messages, cancellation_token=cancellation_token, **kwargs)
        yield result
    
    # Required abstract methods
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
            "provider": "google_mock",
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "function_calling": True,  # Enable function calling for handoffs
            "vision": False,
            "json_output": True
        }
    
    def total_usage(self) -> Any:
        """Return total usage statistics."""
        return None
    
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
