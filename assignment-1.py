from dotenv import load_dotenv
import os
import mysql.connector
import requests
load_dotenv()
conn=0

try:
    # Database Connection
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    print("Connection successful")

    cursor = conn.cursor()

    # Create Table
    query = """
    CREATE TABLE IF NOT EXISTS users(
        id INT PRIMARY KEY,
        name VARCHAR(50),
        username VARCHAR(50),
        email VARCHAR(50)
    )
    """

    cursor.execute(query)
    print("Table created")

    # API Call
    url = "https://jsonplaceholder.typicode.com/users"

    response = requests.get(url, timeout=5)
    users = response.json()

    print("API request successful")

    # Insert Query
    insert_query = """
    INSERT INTO users(id,name,username,email)
    VALUES(%s,%s,%s,%s)
    """

    count = 0

    for user in users:

        id = user["id"]
        name = user["name"]
        username = user["username"]
        email = user["email"]

        values = (id, name, username, email)

        cursor.execute(insert_query, values)

        print(f"{id} {name}")

        count += 1

    conn.commit()

    print(f"\n{count} Users Inserted Successfully")

except requests.exceptions.RequestException as e:
    print("API Error:", e)

except mysql.connector.Error as e:
    print("Database Error:", e)

finally:

    if cursor:
        cursor.close()

    if conn:
        conn.close()

    print("Database Connection Closed")

