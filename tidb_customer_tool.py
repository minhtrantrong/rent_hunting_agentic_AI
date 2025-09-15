import os
import sys
import argparse

# Adjust the path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

# For MySQL connection
import mysql.connector

def get_tidb_connection():
    """Establish connection to TiDB database."""
    try:
        return mysql.connector.connect(
            host=os.getenv("TIDB_HOST"),
            user=os.getenv("TIDB_USER"),
            password=os.getenv("TIDB_PASSWORD"),
            database=os.getenv("TIDB_DATABASE"),
            autocommit=True
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to TiDB: {err}")
        return None

def fetch_apartments(city: str, price_limit: int) -> str:
    """
    Queries the apartments table to find apartments that match the criteria.
    Args:
        city: The city where the apartment is located.
        price_limit: The maximum price of the apartment.
    Returns:
        A string with the matching apartment records.
    """
    try:
        conn = get_tidb_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * FROM rent WHERE address LIKE '%{city}%' AND low_price < {price_limit}"
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            return "No apartments found matching the criteria."
            
        output = []
        for row in results:
            output.append(f"City: {row['city']}, Name: {row['name']}, Address: {row['address']}, Price: {row['price']}, Beds: {row['bed_info']}, Contact Info: {row['phone']}")
        
        cursor.close()
        conn.close()
        return "\n".join(output)

    except Exception as e:
        return f"An error occurred: {e}"

def main():
    parser = argparse.ArgumentParser(description="TiDB Customer Tool")
    parser.add_argument('--apartment', type=str, help='Filter apartments by city and price')
    args = parser.parse_args()

    if args.apartment:
        city, price = args.apartment.split(',')
        price = int(price)
        result = fetch_apartments(city, price)
        print(result)
    else:
        apartments = fetch_apartments()
        print(apartments)

if __name__ == "__main__":
    main()


