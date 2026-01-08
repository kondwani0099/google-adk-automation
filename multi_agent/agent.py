# multi_agent/agent.py
from google.adk.agents import LlmAgent
from multi_agent.conversation import root_agent as conversation_agent
from multi_agent.rag_agent import root_agent as rag_agent

root_agent = LlmAgent(
    name="coordinator",
    model="gemini-2.0-flash",
    description="Routes tasks to appropriate agents.",
    instruction="Route user queries to the conversation agent and rag agent for internal document in the organization.",
    sub_agents=[conversation_agent, rag_agent],
)