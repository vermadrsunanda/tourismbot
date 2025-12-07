# 🤖 Tourism Bot Agent - Quick Start

## What is the Agent?

The AI Agent is an **autonomous system** that uses multiple tools to answer your travel questions. Unlike the basic chat, the agent can:
- 🔍 Analyze your question
- 🛠️ Choose which tools to use
- ⚙️ Execute tools in sequence
- 📊 Compile results into a helpful answer

## Where Can I Use It?

### 1. **Streamlit Web Interface** ⭐ Easiest
```
1. Open streamlit_app.py
2. Click "🤖 AI Agent" tab
3. Ask a question
4. View response + tools used
```

### 2. **REST API** 🔌 For Developers
```bash
curl -X POST http://localhost:5000/api/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What is the weather in Paris?"}'
```

### 3. **Python Code** 🐍 For Integration
```python
from src.agent import TourismAgent

agent = TourismAgent()
result = agent.agentic_loop("Tell me about Tokyo")
print(result['response'])
```

## Example Questions

### Simple Questions (1-2 iterations)
- "What's the weather in Barcelona?"
- "Show me attractions in Rome"
- "Find flights from NYC to London"

### Complex Questions (2-4 iterations)
- "I want to visit Tokyo. Tell me about weather, flights, and attractions"
- "What should I pack for a trip to Amsterdam?"
- "Plan a weekend trip to Berlin"

### Advanced Questions (up to 5 iterations)
- "Compare weather in Paris and London, show me flights from NYC to both, and attractions in each city"
- "I have a budget of $2000. Suggest a destination with flights, weather info, and must-see places"

## How It Works

### Step-by-Step Process

```
Your Question
    ↓
Agent reads your question
    ↓
Mistral AI decides: "Which tools do I need?"
    ↓
Execute Tool 1 (e.g., Weather)  ⤴️ Iterate
Execute Tool 2 (e.g., Flights)  ⤴️ if needed
Execute Tool 3 (e.g., Attractions)
    ↓
Compile all results
    ↓
Final Answer + Tool Details
```

### Tool Availability

| Tool | What It Does | Example |
|------|-------------|---------|
| 🌤️ **Weather** | Get current weather | "It's 15°C, partly cloudy" |
| ✈️ **Flights** | Search flights | "Emirates: $850, departs 10:00" |
| 🎯 **Attractions** | Find attractions | "Eiffel Tower, Louvre Museum" |
| 💡 **Travel Tips** | Travel advice | "Best time to visit is April-May" |
| 💬 **Chat** | General conversation | Regular chat responses |

## Response Example

**Your Question:** 
> "What's the weather in Paris and what are the main attractions?"

**Agent Response:**
```
Paris is a wonderful destination! Currently, it's:

🌤️ Weather:
   • Temperature: 12°C (54°F)
   • Condition: Partly Cloudy
   • Humidity: 65%

🎯 Attractions:
   • Eiffel Tower - iconic iron structure
   • Louvre Museum - world's largest art museum
   • Notre-Dame Cathedral - historic cathedral
   • Arc de Triomphe - monumental arch
   • Sacré-Cœur - basilica in Montmartre

🔧 Tools Used:
   ✅ Weather tool executed
   ✅ Attractions tool executed

📊 Metrics:
   Iterations: 2
   Success: Yes
```

## API Reference

### 1. Submit Query
```
POST /api/agent/query
Content-Type: application/json

{
  "query": "Your question here"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Agent's answer",
  "tools_used": [...],
  "iterations": 2
}
```

### 2. Check Status
```
GET /api/agent/status
```

**Response:**
```json
{
  "status": "active",
  "tools_available": 5,
  "max_iterations": 5,
  "conversation_length": 3
}
```

### 3. Get History
```
GET /api/agent/history
```

**Response:**
```json
{
  "success": true,
  "history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "length": 2
}
```

### 4. Reset Conversation
```
POST /api/agent/reset
```

**Response:**
```json
{
  "success": true,
  "message": "Agent reset successfully"
}
```

## Tips for Best Results

### ✅ DO
- Ask **specific questions** - "Weather in Paris" not "Tell me about Europe"
- Ask **complex questions** - Agent handles multi-step queries
- **Use natural language** - Write like you're talking to a person
- **Check the tools used** - See which tools answered your question

### ❌ DON'T
- Ask about **current news** - Not supported
- Ask about **non-travel topics** - Agent focuses on travel
- Expect **real-time pricing** - Demo data only
- Ask **too broad questions** - "Tell me about the world" won't work well

## Configuration

### Change Max Iterations
Edit `src/agent.py`:
```python
class TourismAgent:
    def __init__(self):
        self.max_iterations = 5  # Change this to 3, 7, etc.
```

### Add New Tools
```python
def _build_tools(self):
    self.tools['custom_tool'] = Tool(
        name='custom_tool',
        description='My custom tool',
        tool_type=ToolType.CHAT,
        parameters={...},
        function=self._tool_custom_function
    )
```

## Troubleshooting

### Agent returns same response every time
- **Solution:** Use `/api/agent/reset` to clear history
- Try asking a different question

### Agent takes too long
- **Solution:** Ask simpler questions (less tools needed)
- Check iterations count - if it's 5, that's the max

### Agent doesn't use any tools
- **Normal!** Some questions don't need external tools
- Agent answered directly from knowledge base

### Tool returns empty result
- **Check:** City/destination name is spelled correctly
- **Try:** Use different city names

## Performance

### Expected Response Times

```
Question Type          Tools Used   Time
─────────────────────────────────────────
Simple (weather)       1            2-3s
Moderate (weather+     2-3          4-6s
  flights)
Complex (all tools)    4-5          6-10s
```

### Limits

- **Max iterations:** 5 per query
- **Max query length:** 1000 characters
- **Timeout:** 30 seconds
- **Concurrent requests:** Unlimited

## Examples

### Example 1: Weather Query
```
Input:  "What's the weather in Tokyo?"
Output: Agent calls WEATHER tool
        Returns: Temperature, conditions, humidity
Time:   ~2 seconds
```

### Example 2: Travel Planning
```
Input:  "Plan a trip to Rome with weather, flights, and attractions"
Output: Agent calls WEATHER, FLIGHTS, ATTRACTIONS
        Returns: Comprehensive travel plan
Time:   ~5 seconds
```

### Example 3: Complex Question
```
Input:  "Compare Barcelona and Madrid - weather, flights from NYC, attractions"
Output: Agent iterates multiple times
        Tool 1: WEATHER Barcelona
        Tool 2: WEATHER Madrid
        Tool 3: FLIGHTS NYC→Barcelona
        Tool 4: FLIGHTS NYC→Madrid
        Tool 5: ATTRACTIONS Barcelona+Madrid
Time:   ~8 seconds
```

## Next Steps

1. **Try it out**: Open Streamlit and click the agent tab
2. **Test the API**: Use curl to test endpoints
3. **Read more**: Check AGENT.md for detailed guide
4. **Deploy**: Share your agent on Streamlit Cloud
5. **Customize**: Add your own tools and features

## Support

**Documentation Files:**
- `AGENT.md` - Complete guide (500+ lines)
- `README.md` - API reference
- `COMMANDS.md` - Command examples

**Test Script:**
```bash
python test_agent.py
```

**Check Logs:**
```bash
tail -f logs/*.log
```

---

## Quick Commands

```bash
# Run the agent
streamlit run streamlit_app.py

# Test the agent
python test_agent.py

# Check status
curl http://localhost:5000/api/agent/status

# Query agent
curl -X POST http://localhost:5000/api/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Tell me about Paris"}'

# Reset agent
curl -X POST http://localhost:5000/api/agent/reset

# Get history
curl http://localhost:5000/api/agent/history
```

---

**Version:** 2.1  
**Status:** ✅ Production Ready  
**Last Updated:** December 2024

**Ready to explore with AI-powered travel assistance!** 🚀
