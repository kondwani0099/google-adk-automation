# agents/agent.py
import sys
import os

# Add the parent directory to the Python path so we can import from multi_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_agent.agent import root_agent

# Export the root_agent for ADK to find
__all__ = ['root_agent']