import sys
import os

import yaml

from city_data_extractor import extract_city_data

# For agent
from agno.agent import Agent
from agno.storage.sqlite import SqliteStorage

# For environment variables
from dotenv import load_dotenv
load_dotenv() # Load environment variables

# Load city data
with open("data/country_and_city_urls.yaml", "r", encoding="utf-8") as file:
    country_and_city_urls = yaml.safe_load(file)

# For model configuration
from models import load_model_instance

# Using Google AI Studio
model_instance = load_model_instance("gemini")

# Store agent sessions in a SQLite database
# Delete the existing database file if it exists
if os.path.exists("tmp/agent.db"):
    os.remove("tmp/agent.db")
# Create the storage
storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")


# Create an agent with the model instance
agent = Agent(
    name="Web Search Agent",
    model=model_instance,
    tools=[extract_city_data], 
    show_tool_calls=True,
    instructions=[
        "Search your knowledge before answering the question.",
        "Use tables to display data.",
        "Include sources in your response.",
        "Generate a brief and concise summary of the search results.",
        "Only include the report in your response. No other text.",
        f"Source: {country_and_city_urls}",
    ],
    storage=storage,
    add_datetime_to_instructions=True,
    # Add the chat history to the messages
    add_history_to_messages=True,
    # Number of history runs
    num_history_runs=3,
    markdown=True,
)

if __name__ == "__main__":
    while True:
        user_input = input("Enter your search query: ")

        if user_input.lower() == "":
            print("Exiting...")
            break

        agent.print_response(
            message=f"{user_input}", 
            markdown=True, 
            stream=True
        )