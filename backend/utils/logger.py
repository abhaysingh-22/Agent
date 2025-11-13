"""
Simple logger utility for tracking agent interactions.
"""
from datetime import datetime


def log_message(message_type: str, content: str, metadata: dict = None):
    """
    Log a message with timestamp and optional metadata.
    
    Args:
        message_type: Type of message (e.g., 'USER_INPUT', 'AGENT_RESPONSE', 'TOOL_CALL')
        content: The actual message content
        metadata: Additional context (optional)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{message_type}] {content}"
    
    if metadata:
        log_entry += f" | Metadata: {metadata}"
    
    print(log_entry)


def log_error(error: Exception, context: str = ""):
    """
    Log an error with context.
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [ERROR] {context}: {str(error)}")


def log_info(message: str):
    """
    Log general information.
    
    Args:
        message: Info message to log
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [INFO] {message}")