import os
import mysql.connector
from agno.tools import tool
from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# The database connection function now reads from the loaded environment variables
def get_tidb_connection():
    """
    Establishes a connection to the TiDB database using environment variables.
    """
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
    Securely queries the apartments table for apartments in a given state below a price limit.
    Args:
        state: The state where the apartment is located.
        price_limit: The maximum price of the apartment.
    Returns:
        A string with the matching apartment records.
    """
    try:
        with get_tidb_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM apartments WHERE state = %s AND price < %s"
                cursor.execute(query, (state, price_limit))
                results = cursor.fetchall()
                if not results:
                    return "No apartments found matching the criteria."
                output = []
                for row in results:
                    output.append(
                        f"State: {row.get('state', '')}, Name: {row.get('name', '')}, "
                        f"Address: {row.get('address', '')}, Price: {row.get('price', '')}, Beds: {row.get('bed_info', '')}"
                    )
                return "\n".join(output)
    except Exception as e:
        return f"An error occurred: {e}"

# The agent creation is unchanged
gemini_model = Gemini(id="gemini-1.5-flash-latest")

agent = Agent(
    model=gemini_model,
    tools=[query_apartments],
    description="You are an agent that can find apartments based on user requests.",
    instructions="You must use the query_apartments tool to find apartments based on the user's criteria for state and price.",
    show_tool_calls=True
)

# Example user message and execution
if __name__ == "__main__":
    user_message = "I would like to find an apartment in Florida with the price less than $1500"
    response = agent.run(user_message)
    print(response)