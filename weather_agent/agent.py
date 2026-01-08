# weather_agent/agent.py
from google.adk.agents import Agent
import datetime
from zoneinfo import ZoneInfo

def get_weather(city: str) -> dict:
    """Mock weather tool for a city."""
    if city.lower() == "lusaka":
        tz = ZoneInfo("Africa/Lusaka")
        now = datetime.datetime.now(tz)
        report = f"Sunny, 20°C in {city} at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        return {"status": "success", "report": report}
    return {"status": "error", "error_message": f"No weather data for {city}."}

root_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    description="Answers weather queries for cities.",
    instruction="Use get_weather to provide accurate weather info.",
    tools=[get_weather],
)