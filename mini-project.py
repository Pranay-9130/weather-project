import os 
import requests
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
conn=mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
print("Database connected")
cursor=conn.cursor()
query=cursor.execute("""
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
);
      
""")
print("Table created successfully")

def check_weather():

    city=input("Enter city:")
    url=f'http://api.weatherapi.com/v1/current.json?key={os.getenv("API_KEY")}&q={city}'

    response=requests.get(url)
    data=response.json()
    print(data)

    print(response.status_code)
    print(response.text)
    city=data["location"]["name"]
    country=data["location"]["country"]

    print("city:",city)
    print("country:",country)

    temperature = data["current"]["temp_c"]
    print("temperature:",temperature)

    humidity = data["current"]["humidity"]
    print("humidity:",humidity)

    wind_speed = data["current"]["wind_kph"]
    print("wind_speed:",wind_speed)

    condition = data["current"]["condition"]["text"]
    print("condition:",condition)

    now=datetime.now()
    search_date=now.date()
    search_time=now.time()
    print(now)
    print(search_date)
    print(search_time)
    raw_response=str(data)

    query = '''
    INSERT INTO weather_reports
    (city,country,temperature,humidity,wind_speed,`condition`,
    search_date,search_time,raw_response)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''

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
    cursor.execute(query,values)
    conn.commit()
    print("Weather data added successfully")

def view_history():
    cursor.execute('''SELECT id, city, temperature, `condition`,
    search_date, search_time
    FROM weather_reports''')
    records=cursor.fetchall()
    print("weather history")
    print("-"*60)
    for row in records:
        print(row)
def last_search():
    cursor.execute('''
select * from weather_reports order by desc where limit 1''')
    record=cursor.fetchone()
    if record:
        print("last weather search")
    else:
        print("No record found")
def hottest_city():
    cursor.execute('''
    select city,temperature from weather_reports order by temperature desc limit 1''')
    record=cursor.fetchone()
    if record:
        print("\nHottest City")
        print("City:", record[0]) 
        print("Temperature:", record[1], "°C")
def coldest_city():
    cursor.execute('''select city,temperature from weather_reports order by temperature asc limit 1''')
    record=cursor.fetchone()
    if record:
        print("\nColdest City") 
        print("City:", record[0]) 
        print("Temperature:", record[1], "°C") 
    else: 
        print("No Records Found")
def total_searches():
    cursor.execute('''
select count(*) from weather_reports''')
    count=cursor.fetchone()[0]
    print(count)
    print()
def delete_history(): 
    confirm = input( "Delete all weather history? (yes/no): " ) 
    if confirm.lower() == "yes": 
       cursor.execute(""" DELETE FROM weather_reports """) 
       conn.commit() 
       print("History Deleted Successfully")
    else: print("Deletion Cancelled") 
def export_history(): 
    cursor.execute(""" SELECT city, temperature, `condition` FROM weather_reports """) 
records = cursor.fetchall() 
with open( "weather_history.txt", "w" ) as file: 
    for row in records: file.write( f"{row[0]} | {row[1]}°C | {row[2]}\n" ) 
    print( "Data Exported To weather_history.txt" )
while True:
    print("===weather data===")
    print("1.check weather")
    print("2.view history")
    print("3.hottest city")
    print("4.Coldest city")
    print("5.total searches")
    print("6.delete history")
    print("7.export history")
    print("8.Exit")
    choice=input("Enter choice:")
    if choice=="1":
        check_weather()
    elif choice=="2":
        view_history()
    elif choice=="3":
        hottest_city()
    elif choice=="4":
        coldest_city()
    elif choice=="5":
        total_searches()
    elif choice=="6":
        delete_history()
    elif choice=="7":
        export_history()
    elif choice=="8":
        print("Thank you!")
        break
    else:
        print("Invalid choice")

cursor.close()
conn.close()






