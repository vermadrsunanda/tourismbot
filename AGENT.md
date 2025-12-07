# 🤖 AI Agent Guide - Tourism Bot

## Overview

The Tourism Bot now includes an **AI Agent** system that autonomously uses multiple tools to answer your travel questions. Unlike the basic chat interface, the agent can:

- 🌤️ Fetch real-time weather data
- ✈️ Search for flight information
- 🎯 Provide attractions and travel tips
- 🔄 Make multiple tool calls in a single conversation
- 📊 Show you exactly which tools were used

## How the Agent Works

### Agentic Loop

The agent operates in an **iterative loop** (max 5 iterations):

1. **User Query**: You ask a question
2. **LLM Decision**: Mistral AI decides what tools are needed
3. **Tool Execution**: The agent executes the necessary tools
4. **Response Generation**: Results are compiled into a helpful answer

### Available Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| **WEATHER** | Get current weather conditions | `city` (string) |
| **FLIGHTS** | Search for flights to a destination | `from_city`, `to_city` (strings) |
| **ATTRACTIONS** | Get popular attractions | `city` (string) |
| **TRAVEL_TIPS** | Get travel advice | `destination` (string) |
| **CHAT** | General conversation | N/A |

## Using the Agent

### Web Interface (Streamlit)

1. Open the app and click the **"🤖 AI Agent"** tab
2. Type your travel question
3. The agent will process your request and show:
   - The complete response
   - Number of iterations used
   - Tools that were executed
   - Details of each tool call

Example queries:
- "What's the weather in Tokyo and what are the attractions?"
- "Find me flights from NYC to London and tell me about the city"
- "Plan a trip to Barcelona with weather, flights, and restaurants"

### API Endpoints

The agent exposes 5 REST API endpoints:

#### `POST /api/agent/query`

Submit a query to the agent.

**Request:**
```json
{
  "query": "What should I know about visiting Rome?"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Rome is an amazing destination...",
  "tools_used": [
    {
      "tool": "attractions",
      "params": {"city": "Rome"},
      "result": {...}
    }
  ],
  "iterations": 2
}
```

#### `GET /api/agent/status`

Get agent status and available tools.

**Response:**
```json
{
  "status": "active",
  "tools_available": ["weather", "flights", "attractions", "travel_tips", "chat"],
  "max_iterations": 5,
  "conversation_length": 3,
  "tools_count": 4
}
```

#### `GET /api/agent/history`

Get the agent's conversation history.

**Response:**
```json
{
  "success": true,
  "history": [
    {"role": "user", "content": "Tell me about Paris"},
    {"role": "assistant", "content": "Paris is..."}
  ],
  "length": 2
}
```

#### `POST /api/agent/reset`

Reset the agent's conversation history.

**Response:**
```json
{
  "success": true,
  "message": "Agent reset successfully"
}
```

#### `GET /api/agent/history`

Retrieve full conversation history.

**Response:**
```json
{
  "success": true,
  "history": [
    {"role": "user", "content": "Query text"},
    {"role": "assistant", "content": "Response text"}
  ],
  "length": 2
}
```

## Examples

### Example 1: Weather Query

**Query:** "What's the weather in Barcelona?"

**Agent Process:**
1. Iteration 1: Calls WEATHER tool for Barcelona
2. Iteration 2: Returns formatted response

**Sample Response:**
```
Barcelona has a Mediterranean climate. Currently, it's typically:
- Temperature: 15-20°C
- Conditions: Partly cloudy
- Humidity: 65%

Best time to visit is April-May or September-October.
```

### Example 2: Complex Travel Planning

**Query:** "I'm planning a trip to Tokyo. Tell me about flights from NYC, weather, and attractions."

**Agent Process:**
1. Iteration 1: LLM identifies need for 3 tools
2. Iteration 2: Executes FLIGHTS tool (NYC → Tokyo)
3. Iteration 3: Executes WEATHER tool (Tokyo)
4. Iteration 4: Executes ATTRACTIONS tool (Tokyo)
5. Final: Compiles all data into comprehensive response

**Tools Used:**
- ✈️ Flights (2-3 airlines with prices)
- 🌤️ Weather (seasonal information)
- 🎯 Attractions (top 5 places to visit)

## Configuration

### Agent Settings

Edit `src/agent.py` to customize:

```python
class TourismAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.max_iterations = 5  # Change max iterations
        self.conversation_history = []  # Conversation tracking
```

### Tool Parameters

Each tool can be customized in the `_build_tools()` method:

```python
def _build_tools(self):
    """Build and register all available tools."""
    self.tools = {
        'weather': Tool(
            name='weather',
            description='Get weather information for a city',
            tool_type=ToolType.WEATHER,
            parameters={'city': 'string'},  # Customize params
            function=self._tool_get_weather
        ),
        # ... more tools
    }
```

## Troubleshooting

### Agent Returns No Tools

If the agent completes without using tools, it means:
- The LLM determined it could answer directly
- No tool calls were detected in the response
- **This is normal!** Not all queries need external tools

### Agent Hits Max Iterations

The agent stops after 5 iterations to prevent infinite loops:
- Highly complex queries may need refinement
- Try asking more specific questions
- Reset the conversation and try again

### Tool Execution Fails

Check the logs for detailed error messages:
```
2025-12-07 11:42:40 - src.agent - ERROR - Tool execution failed: ...
```

Common causes:
- Invalid city names
- API rate limiting
- Network connectivity issues

## Advanced Usage

### Programmatic Access

```python
from src.agent import TourismAgent

agent = TourismAgent()

# Submit query
result = agent.agentic_loop("What's the weather in Paris?")

# Access results
print(result['response'])  # Final answer
print(result['tools_used'])  # List of tools used
print(result['iterations'])  # Number of iterations
```

### Integration with Flask

The agent is already integrated into Flask:

```python
# In src/app.py
from src.agent import TourismAgent

app.tourism_agent = TourismAgent()

@app.route('/api/agent/query', methods=['POST'])
def agent_query():
    query = request.json.get('query')
    result = app.tourism_agent.agentic_loop(query)
    return jsonify(result)
```

### Custom Tools

Add new tools by extending the `TourismAgent` class:

```python
def _tool_custom_function(self, params: Dict) -> str:
    """Custom tool implementation."""
    # Your implementation here
    return "Custom result"

# Register in _build_tools()
self.tools['custom'] = Tool(
    name='custom',
    description='My custom tool',
    tool_type=ToolType.CHAT,
    parameters={...},
    function=self._tool_custom_function
)
```

## Performance

### Typical Response Times

- **Simple queries** (1-2 iterations): 2-4 seconds
- **Complex queries** (3-4 iterations): 4-8 seconds
- **Max iterations** (5 iterations): 8-12 seconds

### Optimization Tips

1. **Specific queries** → Fewer iterations needed
2. **Clear questions** → Better tool selection
3. **Fewer tools** → Faster execution
4. **Lightweight APIs** → Quicker responses

## Monitoring

### Logs

The agent logs all activity:

```
2025-12-07 11:42:40 - src.agent - INFO - Starting agentic loop...
2025-12-07 11:42:41 - src.agent - INFO - Agent iteration 1/5
2025-12-07 11:42:42 - src.agent - INFO - Executed tool 'weather'
2025-12-07 11:42:42 - src.agent - INFO - Agent completed in 2 iterations
```

### Agent Status

Check agent health via the status endpoint:

```bash
curl http://localhost:5000/api/agent/status
```

## Future Enhancements

Potential additions to the agent system:

- 💾 Persistent conversation memory
- 🔐 Multi-user session management
- 📈 Agent performance analytics
- 🎯 Tool usage statistics
- ⚡ Response caching
- 🌍 Multi-language support
- 📱 Voice input integration

## Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Review the troubleshooting section above
3. Test with the `test_agent.py` script
4. Check API endpoint responses directly

---

**Last Updated:** December 2024
**Version:** 2.0
**Status:** Production Ready ✅
