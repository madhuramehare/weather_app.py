
import requests

API_KEY = "58dd3841a7647b8f90f693620a301565"

city = input("Enter city name or ZIP code: ").strip()

if city == "":
    print("Error: City name or ZIP code cannot be empty.")
    exit()

url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": city,
    "appid": API_KEY
}
try:
    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    data = response.json()

    if response.status_code == 401:
        print("Error: Invalid API key.")
        exit()

    elif response.status_code == 404:
        print("Error: City not found.")
        exit()

    elif response.status_code != 200:
        print("Error: Unable to get weather information.")
        exit()

    temperature_c = data["main"]["temp"] - 273.15

    temperature_f = (temperature_c * 9 / 5) + 32

    humidity = data["main"]["humidity"]

    condition = data["weather"][0]["description"]

    wind_speed = data["wind"]["speed"]

    city_name = data["name"]

    country = data["sys"]["country"]

    print("\n" + "=" * 40)
    print("          WEATHER INFORMATION")
    print("=" * 40)

    print(f"Location       : {city_name}, {country}")

    print(f"Temperature    : {temperature_c:.2f} °C")

    print(f"Temperature    : {temperature_f:.2f} °F")

    print(f"Humidity       : {humidity}%")

    print(f"Condition      : {condition.title()}")

    print(f"Wind Speed     : {wind_speed} m/s")

    print("=" * 40)
except requests.exceptions.Timeout:
    print("Error: Request timed out. Please try again.")

except requests.exceptions.ConnectionError:
    print("Error: No internet connection.")

except requests.exceptions.RequestException:
    print("Error: Something went wrong while connecting to the weather API.")

except Exception as e:
    print(f"Error: {e}")

