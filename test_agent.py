import sys
import os
# Adjust the path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

from agno.agent import Agent
from dotenv import load_dotenv
from models import load_model_instance

# Load environment variables
load_dotenv()

# Using Google AI Studio
model_instance = load_model_instance("gemini")

# Create an agent with the model instance
agent = Agent(
    model=model_instance,
    instructions="You are a helpful assistant. Your task is to provide a concise answer.",
    markdown=True,
)

# Print the response in the terminal
agent.print_response("What's Agno agentic framework?")