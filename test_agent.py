#!/usr/bin/env python
"""
Quick test script for the Tourism Agent.
Run with: python test_agent.py
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

from src.agent import TourismAgent

def test_agent():
    """Test the agent with various queries."""
    print("=" * 60)
    print("🤖 Tourism Agent Test Suite")
    print("=" * 60)
    
    try:
        # Initialize agent
        print("\n1️⃣ Initializing agent...")
        agent = TourismAgent()
        print("✅ Agent initialized successfully")
        
        # Test 1: Weather query
        print("\n2️⃣ Test: Weather query")
        print("-" * 60)
        query1 = "What's the weather like in Paris?"
        print(f"Query: {query1}")
        result1 = agent.agentic_loop(query1)
        print(f"Response: {result1['response']}")
        print(f"Tools used: {len(result1['tools_used'])}")
        print(f"Iterations: {result1['iterations']}")
        
        # Reset for next test
        agent.reset_conversation()
        
        # Test 2: Complex travel query
        print("\n3️⃣ Test: Complex travel query")
        print("-" * 60)
        query2 = "I want to go to Tokyo. Can you tell me about flights, weather, and attractions?"
        print(f"Query: {query2}")
        result2 = agent.agentic_loop(query2)
        print(f"Response: {result2['response']}")
        print(f"Tools used: {len(result2['tools_used'])}")
        for tool in result2['tools_used']:
            print(f"  - {tool['tool']}")
        print(f"Iterations: {result2['iterations']}")
        
        # Test 3: Agent status
        print("\n4️⃣ Agent Status")
        print("-" * 60)
        status = agent.get_agent_status()
        print(f"Status: {status}")
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_agent()
    sys.exit(0 if success else 1)
