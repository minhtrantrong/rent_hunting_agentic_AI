import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# The database connection function now reads from the loaded environment variables
def get_tidb_connection():
    return mysql.connector.connect(
        host=os.getenv("TIDB_HOST"),
        user=os.getenv("TIDB_USER"),
        password=os.getenv("TIDB_PASSWORD"),
        database=os.getenv("TIDB_DATABASE")
    )


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
            output.append(f"State: {row['state']}, Name: {row['name']}, Address: {row['address']}, Price: {row['price']}, Beds: {row['bed_info']}")
        
        cursor.close()
        conn.close()
        return "\n".join(output)

    except Exception as e:
        return f"An error occurred: {e}"

response = query_apartments('Florida', 1500)

print(response)