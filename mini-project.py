
import os
import re
import logging
import requests
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()

# ==========================
# Logging Configuration
# ==========================
logging.basicConfig(
    filename="weather.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==========================
# Database Connection
# ==========================
try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = conn.cursor()

    print("Database Connected Successfully")
    logging.info("Database Connected Successfully")

except Exception as e:
    logging.error(f"Database Connection Error: {e}")
    print("Database Connection Failed")
    exit()

# ==========================
# Create Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_reports(
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50),
    country VARCHAR(50),
    temperature FLOAT,
    humidity INT,
    wind_speed FLOAT,
    `condition` VARCHAR(100),
    search_date DATE,
    search_time TIME,
    raw_response TEXT
)
""")

conn.commit()
logging.info("Weather table verified/created")

# ==========================
# Check Weather
# ==========================
def check_weather():

    try:

        city_input = input("Enter City: ").strip()

        # Regex Validation
        if not re.fullmatch(r"[A-Za-z ]{2,50}", city_input):
            print("Invalid City Name")
            logging.warning(f"Invalid City Entered: {city_input}")
            return

        url = f"http://api.weatherapi.com/v1/current.json?key={os.getenv('API_KEY')}&q={city_input}"

        response = requests.get(url)

        data = response.json()

        if "error" in data:
            print("Error:", data["error"]["message"])
            logging.warning(data["error"]["message"])
            return

        city = data["location"]["name"]
        country = data["location"]["country"]

        temperature = data["current"]["temp_c"]
        humidity = data["current"]["humidity"]
        wind_speed = data["current"]["wind_kph"]
        condition = data["current"]["condition"]["text"]

        print("\n" + "-" * 40)
        print("Weather Report")
        print("-" * 40)

        print(f"City        : {city}")
        print(f"Country     : {country}")
        print(f"Temperature : {temperature} °C")
        print(f"Humidity    : {humidity}%")
        print(f"Wind Speed  : {wind_speed} km/h")
        print(f"Condition   : {condition}")

        now = datetime.now()

        search_date = now.date()
        search_time = now.time()

        raw_response = str(data)

        query = """
        INSERT INTO weather_reports
        (
        city,
        country,
        temperature,
        humidity,
        wind_speed,
        `condition`,
        search_date,
        search_time,
        raw_response
        )
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            city,
            country,
            temperature,
            humidity,
            wind_speed,
            condition,
            search_date,
            search_time,
            raw_response
        )

        cursor.execute(query, values)
        conn.commit()

        print("\nWeather Data Saved Successfully")

        logging.info(
            f"Weather searched: {city}, "
            f"Temperature={temperature}, "
            f"Condition={condition}"
        )

    except Exception as e:
        logging.error(str(e))
        print("Error:", e)

# ==========================
# View History
# ==========================
def view_history():

    cursor.execute("""
    SELECT id,
           city,
           temperature,
           `condition`,
           search_date,
           search_time
    FROM weather_reports
    """)

    records = cursor.fetchall()

    if records:

        print("\nWeather History")
        print("-" * 70)

        for row in records:
            print(row)

    else:
        print("No Records Found")

# ==========================
# Last Search
# ==========================
def last_search():

    cursor.execute("""
    SELECT *
    FROM weather_reports
    ORDER BY id DESC
    LIMIT 1
    """)

    record = cursor.fetchone()

    if record:

        print("\nLast Weather Search")
        print("-" * 40)

        print("ID:", record[0])
        print("City:", record[1])
        print("Country:", record[2])
        print("Temperature:", record[3], "°C")
        print("Humidity:", record[4], "%")
        print("Wind Speed:", record[5], "km/h")
        print("Condition:", record[6])
        print("Date:", record[7])
        print("Time:", record[8])

    else:
        print("No Records Found")

# ==========================
# Hottest City
# ==========================
def hottest_city():

    cursor.execute("""
    SELECT city, temperature
    FROM weather_reports
    ORDER BY temperature DESC
    LIMIT 1
    """)

    record = cursor.fetchone()

    if record:
        print("\nHottest City")
        print("City:", record[0])
        print("Temperature:", record[1], "°C")
    else:
        print("No Records Found")

# ==========================
# Coldest City
# ==========================
def coldest_city():

    cursor.execute("""
    SELECT city, temperature
    FROM weather_reports
    ORDER BY temperature ASC
    LIMIT 1
    """)

    record = cursor.fetchone()

    if record:
        print("\nColdest City")
        print("City:", record[0])
        print("Temperature:", record[1], "°C")
    else:
        print("No Records Found")

# ==========================
# Total Searches
# ==========================
def total_searches():

    cursor.execute("""
    SELECT COUNT(*)
    FROM weather_reports
    """)

    count = cursor.fetchone()[0]

    print("\nTotal Weather Searches:", count)

# ==========================
# Delete History
# ==========================
def delete_history():

    confirm = input("Delete all weather history? (yes/no): ")

    if confirm.lower() == "yes":

        cursor.execute("""
        DELETE FROM weather_reports
        """)

        conn.commit()

        logging.info("Weather history deleted")

        print("History Deleted Successfully")

    else:
        print("Deletion Cancelled")

# ==========================
# Export History
# ==========================
def export_history():

    cursor.execute("""
    SELECT city,
           temperature,
           `condition`
    FROM weather_reports
    """)

    records = cursor.fetchall()

    with open("weather_history.txt", "w") as file:

        for row in records:
            file.write(
                f"{row[0]} | {row[1]}°C | {row[2]}\n"
            )

    logging.info("Weather history exported")

    print("Data Exported To weather_history.txt")

# ==========================
# Main Menu
# ==========================
try:

    while True:

        print("\n")
        print("=" * 45)
        print(" WEATHER DATA LOGGER SYSTEM ")
        print("=" * 45)

        print("1. Check Weather")
        print("2. View Weather History")
        print("3. View Last Weather Search")
        print("4. Hottest City Checked")
        print("5. Coldest City Checked")
        print("6. Total Weather Searches")
        print("7. Delete Weather History")
        print("8. Export Weather History")
        print("9. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            check_weather()

        elif choice == "2":
            view_history()

        elif choice == "3":
            last_search()

        elif choice == "4":
            hottest_city()

        elif choice == "5":
            coldest_city()

        elif choice == "6":
            total_searches()

        elif choice == "7":
            delete_history()

        elif choice == "8":
            export_history()

        elif choice == "9":
            print("Thank You")
            break

        else:
            print("Invalid Choice")

finally:

    cursor.close()
    conn.close()

    logging.info("Database Connection Closed")

    print("Database Connection Closed")

