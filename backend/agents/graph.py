"""
LangGraph agent for restaurant assistance.
"""
import os
from typing import TypedDict, Annotated, Sequence
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from .tools import (
    lookup_menu, 
    check_food_stock, 
    get_order_status, 
    place_order, 
    search_faqs,
    update_food_stock
)
from utils.logger import log_info, log_error


# Define the state schema for the agent
class AgentState(TypedDict):
    """State for the restaurant agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]


# System prompt for the restaurant agent
SYSTEM_PROMPT = """You are a friendly restaurant assistant for our Indian restaurant. Your ONLY role is to help customers with restaurant-related queries.

🎯 YOUR RESPONSIBILITIES:
1. Greet customers warmly with Indian hospitality (use phrases like "Namaste!", "Welcome!", etc.)
2. Show the menu from our Google Sheets database
3. Answer questions about our dishes, ingredients, and prices
4. Take orders and provide order confirmations
5. Check order status
6. Answer FAQs about the restaurant (timings, delivery, payments, etc.)
7. Provide food recommendations based on preferences

🚫 STRICT BOUNDARIES - YOU MUST REFUSE:
- Questions about programming, technology, math, science, or any non-restaurant topics
- General knowledge questions (history, geography, definitions, etc.)
- Personal advice or opinions unrelated to food
- Any topic that is NOT about this restaurant, our menu, orders, or food

If someone asks about non-restaurant topics, politely respond with:
"I apologize, but I'm specifically designed to help with our restaurant services only. I can assist you with our menu, orders, timings, and food-related questions. How may I help you with that?"

📋 AVAILABLE TOOLS:
- lookup_menu: Get menu items with prices (₹ INR) from Google Sheets
- check_food_stock: Check ingredient availability  
- get_order_status: Check order status
- place_order: Place customer orders
- search_faqs: Search restaurant FAQs
- update_food_stock: Update inventory (management only)

🎨 PERSONALITY:
- Be warm, friendly, and enthusiastic about food
- Use emojis occasionally (🍛 🥘 🍜 😊)
- Be conversational but stay professional
- Always recommend dishes when appropriate
- Show pride in our authentic Indian cuisine
- Prices are in Indian Rupees (₹)

Remember: You are ONLY a restaurant assistant. Stay in character and refuse all non-restaurant questions politely but firmly."""


class RestaurantAgent:
    """Restaurant agent powered by LangGraph."""
    
    def __init__(self):
        """Initialize the restaurant agent."""
        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # Initialize the language model
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0.7,
            api_key=api_key
        )
        
        # Bind tools to the LLM
        self.tools = [
            lookup_menu, 
            check_food_stock, 
            get_order_status, 
            place_order, 
            search_faqs,
            update_food_stock
        ]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Build the graph
        self.graph = self._build_graph()
        log_info("Restaurant agent initialized successfully")
    
    def _build_graph(self):
        """Build the LangGraph StateGraph."""
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", ToolNode(self.tools))
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )
        
        # Add edge from tools back to agent
        workflow.add_edge("tools", "agent")
        
        # Compile the graph
        return workflow.compile()
    
    def _call_model(self, state: AgentState):
        """Call the language model with the current state."""
        messages = state["messages"]
        
        # Add system message if this is the first interaction
        if len(messages) == 1 and isinstance(messages[0], HumanMessage):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
        # Call the model
        response = self.llm_with_tools.invoke(messages)
        
        # Return the updated state
        return {"messages": [response]}
    
    def _should_continue(self, state: AgentState):
        """Determine if the agent should continue or end."""
        last_message = state["messages"][-1]
        
        # If the last message has tool calls, continue to tools
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"
        
        # Otherwise, end
        return "end"
    
    def process_message(self, user_message: str) -> str:
        """
        Process a user message and return the agent's response.
        
        Args:
            user_message: The user's input message
            
        Returns:
            The agent's response as a string
        """
        try:
            log_info(f"Processing user message: {user_message}")
            
            # Create initial state with user message
            initial_state = {
                "messages": [HumanMessage(content=user_message)]
            }
            
            # Run the graph
            result = self.graph.invoke(initial_state)
            
            # Extract the final response
            final_message = result["messages"][-1]
            response = final_message.content
            
            log_info(f"Agent response: {response}")
            return response
            
        except Exception as e:
            log_error(e, "Error processing message")
            return "I apologize, but I'm having trouble processing your request right now. Please try again."


# Create a singleton instance
_agent_instance = None


def get_agent() -> RestaurantAgent:
    """Get or create the restaurant agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = RestaurantAgent()
    return _agent_instance