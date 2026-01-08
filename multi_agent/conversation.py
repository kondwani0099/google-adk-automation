# multi_agent/conversation.py
from google.adk.agents import Agent
from multi_agent.researcher import root_agent as researcher_agent
# Temporarily disabled RAG agent due to ChromaDB/OpenTelemetry dependency conflict
# from multi_agent.rag_agent import root_agent as rag_agent

root_agent = Agent(
    name="conversation",
    model="gemini-2.0-flash",
    description="Handles user queries by delegating to other agents.",
    instruction="You are a friendly assistant. Delegate research tasks to the researcher agent for web searches and information gathering.",
    sub_agents=[researcher_agent],  # rag_agent temporarily disabled
)