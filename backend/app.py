"""
FastAPI backend for the restaurant agent.
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from agents.graph import get_agent
from utils.logger import log_message, log_error, log_info

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Restaurant Agent API",
    description="AI-powered restaurant assistant using LangGraph",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request and Response models
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What appetizers do you have?"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    reply: str
    success: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "reply": "We have delicious appetizers including Bruschetta, Mozzarella Sticks, and Caesar Salad!",
                "success": True
            }
        }


@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup."""
    log_info("Starting up Restaurant Agent API...")
    try:
        # Initialize the agent (this will validate the API key)
        get_agent()
        log_info("Restaurant Agent API is ready!")
    except Exception as e:
        log_error(e, "Failed to initialize agent")
        raise


@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {
        "message": "Restaurant Agent API is running",
        "status": "healthy",
        "endpoints": {
            "chat": "POST /chat",
            "health": "GET /health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that processes user messages through the LangGraph agent.
    
    Args:
        request: ChatRequest containing the user's message
        
    Returns:
        ChatResponse containing the agent's reply
    """
    try:
        # Log incoming message
        log_message("USER_INPUT", request.message)
        
        # Get the agent instance
        agent = get_agent()
        
        # Process the message through the agent
        reply = agent.process_message(request.message)
        
        # Log agent response
        log_message("AGENT_RESPONSE", reply)
        
        return ChatResponse(
            reply=reply,
            success=True
        )
        
    except Exception as e:
        # Log the error
        log_error(e, "Error in chat endpoint")
        
        # Return error response
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your message. Please try again."
        )


if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    port = int(os.getenv("PORT", 8000))
    log_info(f"Starting server on port {port}")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=True  # Enable auto-reload during development
    )