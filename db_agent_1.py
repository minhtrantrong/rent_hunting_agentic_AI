import os
import mysql.connector
from agno.tools import tool
from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv

load_dotenv()

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

@tool
def query_apartments(
    state: str = None,
    min_price: int = None,
    max_price: int = None,
    beds: int = None,
    keyword: str = None,
    phone: str = None
) -> str:
    """
    Truy vấn bảng apartments với các điều kiện tùy chọn.
    Args:
        state: Tên bang (State)
        min_price: Giá tối thiểu
        max_price: Giá tối đa
        beds: Số giường ngủ
        keyword: Từ khóa tìm trong Name hoặc Address
        phone: Số điện thoại
    Returns:
        Danh sách kết quả dạng string
    """
    try:
        with get_tidb_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM apartments WHERE 1=1"
                params = []

                if state:
                    query += " AND state = %s"
                    params.append(state)
                if min_price is not None:
                    query += " AND price >= %s"
                    params.append(min_price)
                if max_price is not None:
                    query += " AND price <= %s"
                    params.append(max_price)
                if beds is not None:
                    query += " AND bed_info LIKE %s"
                    params.append(f"{beds} Beds%")
                if keyword:
                    query += " AND (name LIKE %s OR address LIKE %s)"
                    params.extend([f"%{keyword}%", f"%{keyword}%"])
                if phone:
                    query += " AND phone = %s"
                    params.append(phone)

                cursor.execute(query, tuple(params))
                results = cursor.fetchall()

                if not results:
                    return "No apartments found matching the criteria."

                output = []
                for row in results:
                    output.append(
                        f"State: {row.get('state', '')}, "
                        f"Name: {row.get('name', '')}, "
                        f"Address: {row.get('address', '')}, "
                        f"Price: {row.get('price', '')}, "
                        f"Beds: {row.get('bed_info', '')}, "
                        f"Phone: {row.get('phone', '')}, "
                        f"Low Price: {row.get('low_price', '')}, "
                        f"High Price: {row.get('high_price', '')}"
                    )
                return "\n".join(output)
    except Exception as e:
        return f"An error occurred: {e}"

gemini_model = Gemini(id="gemini-1.5-flash-latest")

agent = Agent(
    model=gemini_model,
    tools=[query_apartments],
    description="You are an agent that can find apartments based on various user criteria such as state, price range, beds, and keywords.",
    instructions="You must use the query_apartments tool to find apartments based on the user's criteria.",
    show_tool_calls=True
)

# Ví dụ
if __name__ == "__main__":
    user_message = "Find apartments in Alabama priced between 1500 and 2000 with 3 beds"
    response = agent.run(user_message)
    print(response)
