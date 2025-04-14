# multi_agent/researcher.py
from google.adk.agents import Agent

def google_search(query: str) -> dict:
    """Mock Google search tool."""
    return {"status": "success", "result": f"Search results for '{query}': Sample data."}

root_agent = Agent(
    name="researcher",
    model="gemini-2.0-flash",
    description="Fetches information using search tools.",
    instruction="Use the google_search tool to find information and summarize it.",
    tools=[google_search],
)