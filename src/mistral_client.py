"""
Mistral AI client wrapper for tourism bot interactions.
"""
import os
from typing import Optional
from src.logger import setup_logger

logger = setup_logger(__name__)


class MistralTourismBot:
    """Wrapper for Mistral AI tourism bot."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Mistral AI client.
        
        Args:
            api_key: Mistral API key (defaults to environment variable)
        
        Raises:
            ValueError: If API key is not provided or found
        """
        self.api_key = api_key or os.getenv('MISTRAL_API_KEY')
        
        if not self.api_key:
            logger.error("Mistral API key not found in configuration")
            raise ValueError("MISTRAL_API_KEY is required")
        
        # Initialize Mistral client
        try:
            from mistralai.client import MistralClient
            from mistralai.models.chat_completion import ChatMessage
            self.client = MistralClient(api_key=self.api_key)
            self.ChatMessage = ChatMessage
            logger.info("Mistral AI client initialized successfully")
        except ImportError:
            logger.error("mistralai package not installed")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Mistral client: {str(e)}")
            raise
    
    def generate_tourism_response(self, user_query: str, context: Optional[str] = None) -> str:
        """
        Generate a tourism-related response using Mistral AI.
        
        Args:
            user_query: User's tourism question
            context: Optional context for the conversation
        
        Returns:
            Generated response from Mistral AI
        """
        if not user_query or not isinstance(user_query, str):
            logger.warning("Invalid user query received")
            return "I'm sorry, I didn't understand your question. Please ask about tourism destinations, travel tips, or local attractions."
        
        user_query = user_query.strip()
        
        if len(user_query) > 1000:
            logger.warning("User query exceeds maximum length")
            return "Your question is too long. Please ask a more concise question."
        
        try:
            system_prompt = """You are a helpful tourism assistant chatbot. Your role is to:
- Provide information about popular tourism destinations
- Suggest travel tips and travel planning advice
- Help with information about local attractions, restaurants, and accommodations
- Answer questions about visa requirements, transportation, and travel safety
- Be friendly, informative, and encouraging about travel experiences

Keep responses concise, helpful, and focused on tourism-related topics."""
            
            messages = [
                self.ChatMessage(role="system", content=system_prompt),
                self.ChatMessage(role="user", content=user_query)
            ]
            
            response = self.client.chat(
                model="mistral-small",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            logger.info(f"Successfully generated response for query: {user_query[:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"Error generating response from Mistral: {str(e)}")
            return "I apologize, but I encountered an error while processing your request. Please try again later."
    
    def get_destination_recommendations(self, preferences: str) -> str:
        """
        Get destination recommendations based on user preferences.
        
        Args:
            preferences: User's travel preferences
        
        Returns:
            Destination recommendations
        """
        if not preferences:
            return "Please describe your travel preferences so I can recommend suitable destinations."
        
        query = f"Based on these preferences: {preferences}, recommend 3 suitable tourism destinations and explain why each would be a good fit."
        
        return self.generate_tourism_response(query)
