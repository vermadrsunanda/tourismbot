"""
Integration with external APIs for weather and flight data.
"""
import os
import requests
from typing import Dict, List, Optional
from src.logger import setup_logger

logger = setup_logger(__name__)


class WeatherAPI:
    """Weather data integration using OpenWeatherMap API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Weather API client.
        
        Args:
            api_key: OpenWeatherMap API key (optional for demo mode)
        """
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.demo_mode = not self.api_key
    
    def get_weather(self, city: str) -> Optional[Dict]:
        """
        Get weather data for a city.
        
        Args:
            city: City name
        
        Returns:
            Weather data or None if error
        """
        if not city:
            return None
        
        # Demo mode with sample data
        if self.demo_mode:
            logger.info(f"Demo mode: Returning sample weather for {city}")
            return self._get_demo_weather(city)
        
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'destination': city,
                    'temperature': round(data['main']['temp']),
                    'description': data['weather'][0]['main'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'success': True
                }
            else:
                logger.warning(f"Weather API error for {city}: {response.status_code}")
                return self._get_demo_weather(city)
                
        except Exception as e:
            logger.error(f"Error fetching weather for {city}: {str(e)}")
            return self._get_demo_weather(city)
    
    def _get_demo_weather(self, city: str) -> Dict:
        """Get demo weather data."""
        demo_data = {
            'paris': {'temp': 12, 'desc': 'Partly Cloudy'},
            'bangkok': {'temp': 32, 'desc': 'Humid and Warm'},
            'tokyo': {'temp': 15, 'desc': 'Sunny'},
            'bali': {'temp': 28, 'desc': 'Sunny'},
            'dubai': {'temp': 35, 'desc': 'Hot and Dry'},
            'london': {'temp': 10, 'desc': 'Rainy'},
            'new york': {'temp': 18, 'desc': 'Partly Cloudy'},
            'sydney': {'temp': 22, 'desc': 'Sunny'},
        }
        
        city_lower = city.lower()
        weather = demo_data.get(city_lower, {'temp': 20, 'desc': 'Pleasant'})
        
        return {
            'destination': city,
            'temperature': weather['temp'],
            'description': weather['desc'],
            'humidity': 65,
            'wind_speed': 5,
            'success': True
        }


class FlightAPI:
    """Flight data integration using demo/mock API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Flight API client.
        
        Args:
            api_key: Flight API key (optional for demo mode)
        """
        self.api_key = api_key or os.getenv('FLIGHT_API_KEY')
        self.demo_mode = True  # Using demo mode by default
    
    def search_flights(self, origin: str, destination: str) -> Optional[Dict]:
        """
        Search for flights between two cities.
        
        Args:
            origin: Origin city
            destination: Destination city
        
        Returns:
            Flight data or None if error
        """
        if not origin or not destination:
            return None
        
        # Using demo mode with sample flights
        logger.info(f"Demo mode: Returning sample flights from {origin} to {destination}")
        return self._get_demo_flights(origin, destination)
    
    def _get_demo_flights(self, origin: str, destination: str) -> Dict:
        """Generate demo flight data."""
        airlines = [
            {'name': 'Emirates', 'code': 'EK'},
            {'name': 'Qatar Airways', 'code': 'QR'},
            {'name': 'Singapore Airlines', 'code': 'SQ'},
            {'name': 'Lufthansa', 'code': 'LH'},
            {'name': 'British Airways', 'code': 'BA'},
        ]
        
        flights = []
        for i, airline in enumerate(airlines):
            flights.append({
                'airline': airline['name'],
                'code': airline['code'],
                'departure': f"{origin} 10:{i*2:02d}",
                'arrival': f"{destination} 18:{i*2:02d}",
                'price': 250 + (i * 100),
                'duration': '8h 30m'
            })
        
        return {
            'origin': origin,
            'destination': destination,
            'flights': flights,
            'success': True
        }


class TourismDataAPI:
    """Integration with tourism-related data."""
    
    @staticmethod
    def get_popular_attractions(city: str) -> Dict:
        """
        Get popular attractions for a city.
        
        Args:
            city: City name
        
        Returns:
            Attractions data
        """
        attractions_db = {
            'paris': [
                'Eiffel Tower',
                'Louvre Museum',
                'Notre-Dame Cathedral',
                'Arc de Triomphe',
                'Sacré-Cœur'
            ],
            'tokyo': [
                'Senso-ji Temple',
                'Tokyo Skytree',
                'Shibuya Crossing',
                'Meiji Shrine',
                'Imperial Palace'
            ],
            'new york': [
                'Statue of Liberty',
                'Central Park',
                'Times Square',
                'Empire State Building',
                'Brooklyn Bridge'
            ],
            'bali': [
                'Tanah Lot Temple',
                'Ubud Palace',
                'Mount Batur',
                'Seminyak Beach',
                'Tegallalang Rice Terraces'
            ],
            'london': [
                'Big Ben',
                'Tower of London',
                'Buckingham Palace',
                'Westminster Abbey',
                'Tower Bridge'
            ]
        }
        
        city_lower = city.lower()
        attractions = attractions_db.get(
            city_lower,
            ['Local Museums', 'Historical Sites', 'Parks', 'Restaurants', 'Shopping Areas']
        )
        
        return {
            'city': city,
            'attractions': attractions,
            'success': True
        }
    
    @staticmethod
    def get_travel_tips(destination: str) -> Dict:
        """
        Get travel tips for a destination.
        
        Args:
            destination: Destination name
        
        Returns:
            Travel tips
        """
        tips = [
            'Check visa requirements before traveling',
            'Book accommodations in advance during peak season',
            'Learn basic phrases in the local language',
            'Purchase travel insurance',
            'Inform your bank about international travel',
            'Download offline maps',
            'Research local customs and etiquette',
            'Pack light and smart'
        ]
        
        return {
            'destination': destination,
            'tips': tips,
            'success': True
        }
