"""
AI Agent system for Tourism Bot.
Implements an agentic loop with tool capabilities.
"""
import json
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass
from src.logger import setup_logger
from src.external_apis import WeatherAPI, FlightAPI, TourismDataAPI
from src.mistral_client import MistralTourismBot

logger = setup_logger(__name__)


class ToolType(Enum):
    """Available tool types."""
    WEATHER = "weather"
    FLIGHTS = "flights"
    ATTRACTIONS = "attractions"
    TRAVEL_TIPS = "travel_tips"
    CHAT = "chat"


@dataclass
class Tool:
    """Tool definition."""
    name: str
    description: str
    tool_type: ToolType
    parameters: Dict[str, Any]
    function: Callable


@dataclass
class ToolResult:
    """Result from tool execution."""
    tool_name: str
    success: bool
    result: Any
    error: Optional[str] = None


class TourismAgent:
    """
    AI Agent for tourism planning with tool capabilities.
    Uses an agentic loop to handle user requests.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Tourism Agent.
        
        Args:
            api_key: Mistral AI API key
        """
        self.mistral_bot = MistralTourismBot(api_key)
        self.weather_api = WeatherAPI()
        self.flight_api = FlightAPI()
        self.max_iterations = 5
        self.conversation_history = []
        
        # Initialize available tools
        self._initialize_tools()
        
        logger.info("Tourism Agent initialized successfully")
    
    def _initialize_tools(self):
        """Initialize available tools for the agent."""
        self.tools = {
            ToolType.WEATHER: Tool(
                name="get_weather",
                description="Get current weather for a destination",
                tool_type=ToolType.WEATHER,
                parameters={
                    "destination": {
                        "type": "string",
                        "description": "City or destination name"
                    }
                },
                function=self._tool_get_weather
            ),
            ToolType.FLIGHTS: Tool(
                name="search_flights",
                description="Search for flights between two cities",
                tool_type=ToolType.FLIGHTS,
                parameters={
                    "origin": {
                        "type": "string",
                        "description": "Origin city"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Destination city"
                    }
                },
                function=self._tool_search_flights
            ),
            ToolType.ATTRACTIONS: Tool(
                name="get_attractions",
                description="Get popular attractions for a destination",
                tool_type=ToolType.ATTRACTIONS,
                parameters={
                    "city": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                function=self._tool_get_attractions
            ),
            ToolType.TRAVEL_TIPS: Tool(
                name="get_travel_tips",
                description="Get travel tips for a destination",
                tool_type=ToolType.TRAVEL_TIPS,
                parameters={
                    "destination": {
                        "type": "string",
                        "description": "Destination name"
                    }
                },
                function=self._tool_get_travel_tips
            ),
        }
    
    # Tool implementations
    def _tool_get_weather(self, destination: str) -> Dict:
        """Get weather for a destination."""
        try:
            result = self.weather_api.get_weather(destination)
            return {
                "success": True,
                "data": result
            }
        except Exception as e:
            logger.error(f"Weather tool error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _tool_search_flights(self, origin: str, destination: str) -> Dict:
        """Search for flights."""
        try:
            result = self.flight_api.search_flights(origin, destination)
            return {
                "success": True,
                "data": result
            }
        except Exception as e:
            logger.error(f"Flight tool error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _tool_get_attractions(self, city: str) -> Dict:
        """Get attractions for a city."""
        try:
            result = TourismDataAPI.get_popular_attractions(city)
            return {
                "success": True,
                "data": result
            }
        except Exception as e:
            logger.error(f"Attractions tool error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _tool_get_travel_tips(self, destination: str) -> Dict:
        """Get travel tips for a destination."""
        try:
            result = TourismDataAPI.get_travel_tips(destination)
            return {
                "success": True,
                "data": result
            }
        except Exception as e:
            logger.error(f"Travel tips tool error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_tools_description(self) -> str:
        """Build description of available tools for the agent."""
        tools_desc = "Available tools:\n\n"
        for tool_type, tool in self.tools.items():
            tools_desc += f"- {tool.name}: {tool.description}\n"
            tools_desc += f"  Parameters: {json.dumps(tool.parameters, indent=2)}\n\n"
        return tools_desc
    
    def _parse_agent_response(self, response: str) -> tuple[Optional[str], Optional[Dict]]:
        """
        Parse agent response to extract tool call if present.
        
        Expected format:
        TOOL: tool_name
        PARAMS: {"param1": "value1"}
        RESPONSE: The response text
        """
        lines = response.split('\n')
        tool_name = None
        params = None
        response_text = response
        
        try:
            for i, line in enumerate(lines):
                if line.startswith('TOOL:'):
                    tool_name = line.replace('TOOL:', '').strip()
                elif line.startswith('PARAMS:'):
                    params_str = line.replace('PARAMS:', '').strip()
                    params = json.loads(params_str)
                elif line.startswith('RESPONSE:'):
                    response_text = '\n'.join(lines[i:]).replace('RESPONSE:', '').strip()
                    break
        except Exception as e:
            logger.warning(f"Error parsing agent response: {str(e)}")
            return None, None
        
        return tool_name, params
    
    def execute_tool(self, tool_name: str, params: Dict) -> ToolResult:
        """
        Execute a tool with given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            params: Parameters for the tool
        
        Returns:
            ToolResult with execution results
        """
        try:
            # Find tool by name
            tool = None
            for t in self.tools.values():
                if t.name == tool_name:
                    tool = t
                    break
            
            if not tool:
                return ToolResult(
                    tool_name=tool_name,
                    success=False,
                    result=None,
                    error=f"Tool '{tool_name}' not found"
                )
            
            # Execute tool
            result = tool.function(**params)
            
            logger.info(f"Tool '{tool_name}' executed successfully")
            return ToolResult(
                tool_name=tool_name,
                success=result.get("success", False),
                result=result.get("data"),
                error=result.get("error")
            )
            
        except Exception as e:
            logger.error(f"Error executing tool '{tool_name}': {str(e)}")
            return ToolResult(
                tool_name=tool_name,
                success=False,
                result=None,
                error=str(e)
            )
    
    def agentic_loop(self, user_query: str) -> Dict:
        """
        Execute the agentic loop to handle user query.
        
        Args:
            user_query: User's query
        
        Returns:
            Dictionary with final response and executed tools
        """
        logger.info(f"Starting agentic loop for query: {user_query[:50]}...")
        
        # Store in conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_query
        })
        
        tool_results = []
        iteration = 0
        
        # Agentic loop
        while iteration < self.max_iterations:
            iteration += 1
            logger.info(f"Agent iteration {iteration}/{self.max_iterations}")
            
            # Build system prompt with tools
            system_prompt = f"""You are a helpful tourism planning agent.
You have access to the following tools to help answer questions:

{self._build_tools_description()}

When you need to use a tool, format your response as:
TOOL: tool_name
PARAMS: {{"param1": "value1"}}
RESPONSE: Your response text

If you don't need tools, just provide the response directly.

Always try to help the user with accurate information.
"""
            
            # Get agent response from Mistral
            try:
                messages = [{"role": "system", "content": system_prompt}]
                for msg in self.conversation_history[-3:]:  # Use last 3 messages for context
                    messages.append(msg)
                
                agent_response = self.mistral_bot.generate_tourism_response(
                    user_query,
                    context=f"Previous tools used: {tool_results}"
                )
                
                # Parse response for tool calls
                tool_name, params = self._parse_agent_response(agent_response)
                
                if tool_name and params:
                    logger.info(f"Agent decided to use tool: {tool_name}")
                    
                    # Execute tool
                    tool_result = self.execute_tool(tool_name, params)
                    tool_results.append({
                        "tool": tool_name,
                        "params": params,
                        "result": tool_result.result if tool_result.success else tool_result.error
                    })
                    
                    # Add to conversation history
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": f"Used tool {tool_name}"
                    })
                    self.conversation_history.append({
                        "role": "tool",
                        "content": str(tool_result.result)
                    })
                else:
                    # No tool needed, return final response
                    logger.info("Agent completed with direct response")
                    
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": agent_response
                    })
                    
                    return {
                        "success": True,
                        "response": agent_response,
                        "tools_used": tool_results,
                        "iterations": iteration
                    }
            
            except Exception as e:
                logger.error(f"Error in agentic loop: {str(e)}")
                return {
                    "success": False,
                    "response": f"Error: {str(e)}",
                    "tools_used": tool_results,
                    "iterations": iteration
                }
        
        # Max iterations reached
        logger.warning(f"Agent reached max iterations ({self.max_iterations})")
        return {
            "success": False,
            "response": "Agent reached maximum iterations",
            "tools_used": tool_results,
            "iterations": iteration
        }
    
    def process_query(self, user_query: str) -> str:
        """
        Process user query through the agent.
        
        Args:
            user_query: User's query
        
        Returns:
            Final response from agent
        """
        try:
            result = self.agentic_loop(user_query)
            
            if result["success"]:
                return result["response"]
            else:
                return f"I encountered an error: {result['response']}"
        
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return f"Sorry, I couldn't process your request: {str(e)}"
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []
        logger.info("Conversation history reset")
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history."""
        return self.conversation_history
    
    def get_agent_status(self) -> Dict:
        """Get agent status information."""
        return {
            "status": "active",
            "tools_available": list(self.tools.keys()),
            "max_iterations": self.max_iterations,
            "conversation_length": len(self.conversation_history),
            "tools_count": len(self.tools)
        }
