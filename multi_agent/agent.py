# multi_agent/agent.py
from google.adk.agents import LlmAgent
from multi_agent.conversation import root_agent as conversation_agent

root_agent = LlmAgent(
    name="coordinator",
    model="gemini-2.0-flash",
    description="Routes tasks to appropriate agents.",
    instruction="Route user queries to the conversation agent.",
    sub_agents=[conversation_agent],
)