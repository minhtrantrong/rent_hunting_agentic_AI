import os
import mysql.connector
from agno.tools import tool
from agno.agent import Agent
from agno.storage.sqlite import SqliteStorage
from agno.models.google import Gemini
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Store agent sessions in a SQLite database
# Delete the existing database file if it exists
if os.path.exists("tmp/agent.db"):
    os.remove("tmp/agent.db")
# Create the storage
storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")


# The database connection function now reads from the loaded environment variables
def get_tidb_connection():
    return mysql.connector.connect(
        host=os.getenv("TIDB_HOST"),
        user=os.getenv("TIDB_USER"),
        password=os.getenv("TIDB_PASSWORD"),
        database=os.getenv("TIDB_DATABASE")
    )

# The tool definition is unchanged as it relies on the get_tidb_connection function
@tool
def query_apartments(state: str, price_limit: int) -> str:
    """
    Queries the apartments table to find apartments that match the criteria.
    Args:
        state: The state where the apartment is located.
        price_limit: The maximum price of the apartment.
    Returns:
        A string with the matching apartment records.
    """
    try:
        conn = get_tidb_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * FROM rent WHERE State = '{state}' AND low_price < {price_limit}"
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            return "No apartments found matching the criteria."
            
        output = []
        for row in results:
            output.append(f"State: {row['state']}, Name: {row['name']}, Address: {row['address']}, Price: {row['price']}, Beds: {row['bed_info']}, Contact Info: {row['phone']}")
        
        cursor.close()
        conn.close()
        return "\n".join(output)

    except Exception as e:
        return f"An error occurred: {e}"

# The agent creation is unchanged
gemini_model = Gemini(id="gemini-1.5-flash-latest")

agent = Agent(
    name="Apartment Finder",
    model=gemini_model,
    tools=[query_apartments],
    description="An agent that helps users find apartments based on their criteria.",
    instructions=[
        "You are an expert in finding apartments.",
        "Use the provided tool to query the database for apartments based on user criteria.",
        "Always ask for the state and price limit before querying.",
        "When providing customer data, format it in table.",
    ],
    show_tool_calls=True,
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
        user_input = input("User: ")

        if user_input.lower() == "":
            print("Exiting...")
            break

        agent.print_response(
            message=f"{user_input}", 
            markdown=True, 
        )
    
    # Sample prompt: "I would like to find an apartment in Florida with the price less than $1500"