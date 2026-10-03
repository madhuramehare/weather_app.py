import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime

API_KEY = "58dd3841a7647b8f90f693620a301565"

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
IP_LOCATION_URL = "https://ipinfo.io/json"

unit = "metric"
current_city = ""
icon_references = []

def show_error(message):
    error_label.config(text=message)
    city_label.config(text="")
    current_weather_label.config(text="")
    current_icon_label.config(image="")
    
    for widget in hourly_frame.winfo_children():
        widget.destroy()

    for widget in daily_frame.winfo_children():
        widget.destroy()

def clear_error():
    error_label.config(text="")

def get_weather():
    global current_city

    city = city_entry.get().strip()

    if not city:
        show_error("Please enter a city name.")
        return

    if API_KEY == "YOUR_API_KEY_HERE":
        show_error("Please add your OpenWeatherMap API key in the code.")
        return

    clear_error()
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": unit
        }

        response = requests.get(
            CURRENT_WEATHER_URL,
            params=params,
            timeout=10
        )

        data = response.json()

        if response.status_code != 200:
            show_error(data.get("message", "Unable to get weather data."))
            return

        current_city = data["name"]

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        description = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]

        symbol = "°C" if unit == "metric" else "°F"

        city_label.config(
            text=f"{current_city}, {data['sys']['country']}"
        )

        current_weather_label.config(
            text=(
                f"{temperature:.1f}{symbol}\n"
                f"{description.title()}\n\n"
                f"Feels Like: {feels_like:.1f}{symbol}\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s"
            )
        )

        load_weather_icon(icon_code, current_icon_label)
        get_forecast(current_city)

    except requests.exceptions.ConnectionError:
        show_error("No internet connection. Please check your network.")

    except requests.exceptions.Timeout:
        show_error("Request timed out. Please try again.")

    except Exception as e:
        show_error(f"Error: {str(e)}")

def load_weather_icon(icon_code, label):
    try:
        url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

        response = requests.get(url, timeout=10)

        image = Image.open(BytesIO(response.content))
        image = image.resize((100, 100))

        photo = ImageTk.PhotoImage(image)

        label.config(image=photo)
        label.image = photo

        icon_references.append(photo)

    except Exception:
        label.config(image="")
def get_forecast(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": unit
        }

        response = requests.get(
            FORECAST_URL,
            params=params,
            timeout=10
        )

        data = response.json()

        if response.status_code != 200:
            show_error(data.get("message", "Forecast unavailable."))
            return
        create_hourly_forecast(data)
        create_daily_forecast(data)

    except Exception as e:
        show_error(f"Forecast error: {str(e)}")

def create_hourly_forecast(data):

    for widget in hourly_frame.winfo_children():
        widget.destroy()

    symbol = "°C" if unit == "metric" else "°F"

    forecast_list = data["list"][:2]
    for item in forecast_list:

        time_text = datetime.fromtimestamp(
            item["dt"]
        ).strftime("%I:%M %p")

        temperature = item["main"]["temp"]
        description = item["weather"][0]["description"]
        icon_code = item["weather"][0]["icon"]

        card = tk.Frame(
            hourly_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=12,
            pady=8
        )

        card.pack(
            side="left",
            padx=8,
            pady=5
        )

        time_label = tk.Label(
            card,
            text=time_text,
            font=("Arial", 10, "bold"),
            bg="white"
        )

        time_label.pack()

        icon_label = tk.Label(
            card,
            bg="white"
        )

        icon_label.pack()

        load_weather_icon(icon_code, icon_label)

        temp_label = tk.Label(
            card,
            text=f"{temperature:.1f}{symbol}",
            font=("Arial", 12, "bold"),
            bg="white"
        )

        temp_label.pack()

        desc_label = tk.Label(
            card,
            text=description.title(),
            bg="white",
            wraplength=100
        )
        desc_label.pack()

def create_daily_forecast(data):

    for widget in daily_frame.winfo_children():
        widget.destroy()

    symbol = "°C" if unit == "metric" else "°F"

    daily_data = {}

    for item in data["list"]:

        date = datetime.fromtimestamp(
            item["dt"]
        ).strftime("%Y-%m-%d")

        if date not in daily_data:
            daily_data[date] = []

        daily_data[date].append(item)
    dates = list(daily_data.keys())[:5]

    for date in dates:
        items = daily_data[date]

        temperatures = [
            item["main"]["temp"]
            for item in items
        ]

        average_temperature = sum(temperatures) / len(temperatures)
        selected_item = items[len(items) // 2]

        description = selected_item["weather"][0]["description"]
        icon_code = selected_item["weather"][0]["icon"]

        day_name = datetime.strptime(
            date,
            "%Y-%m-%d"
        ).strftime("%A")

        card = tk.Frame(
            daily_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=10,
            pady=8
        )
        card.pack(
            side="left",
            padx=5,
            pady=5
        )
        day_label = tk.Label(
            card,
            text=day_name,
            font=("Arial", 10, "bold"),
            bg="white"
        )

        day_label.pack()
        date_label = tk.Label(
            card,
            text=date,
            bg="white"
        )

        date_label.pack()
        icon_label = tk.Label(
            card,
            bg="white"
        )

        icon_label.pack()

        load_weather_icon(icon_code, icon_label)
        temp_label = tk.Label(
            card,
            text=f"{average_temperature:.1f}{symbol}",
            font=("Arial", 12, "bold"),
            bg="white"
        )

        temp_label.pack()

        desc_label = tk.Label(
            card,
            text=description.title(),
            bg="white",
            wraplength=100
        )

        desc_label.pack()

def toggle_unit():
    global unit

    if unit == "metric":
        unit = "imperial"
        unit_button.config(text="Switch to °C")
    else:
        unit = "metric"
        unit_button.config(text="Switch to °F")

    if current_city:
        city_entry.delete(0, tk.END)
        city_entry.insert(0, current_city)
        get_weather()

def detect_location():
    try:

        response = requests.get(
            IP_LOCATION_URL,
            timeout=10
        )

        data = response.json()
        city = data.get("city")

        if not city:
            show_error("Could not detect your location.")
            return

        city_entry.delete(0, tk.END)
        city_entry.insert(0, city)

        get_weather()

    except requests.exceptions.ConnectionError:
        show_error("Unable to detect location. Check your internet.")

    except Exception:
        show_error("Automatic location detection failed.")

root = tk.Tk()

root.title("Advanced Weather App")
root.geometry("1050x800")
root.configure(bg="#eaf4ff")
title_label = tk.Label(
    root,
    text="🌤 Advanced Weather App",
    font=("Arial", 24, "bold"),
    bg="#eaf4ff"
)

title_label.pack(pady=15)

search_frame = tk.Frame(
    root,
    bg="#eaf4ff"
)

search_frame.pack(pady=5)

city_entry = tk.Entry(
    search_frame,
    width=30,
    font=("Arial", 14)
)
city_entry.grid(
    row=0,
    column=0,
    padx=5
)

get_button = tk.Button(
    search_frame,
    text="Get Weather",
    font=("Arial", 11, "bold"),
    command=get_weather
)

get_button.grid(
    row=0,
    column=1,
    padx=5
)

location_button = tk.Button(
    search_frame,
    text="📍 Detect Location",
    font=("Arial", 11, "bold"),
    command=detect_location
)
location_button.grid(
    row=0,
    column=2,
    padx=5
)

unit_button = tk.Button(
    search_frame,
    text="Switch to °F",
    font=("Arial", 11, "bold"),
    command=toggle_unit
)

unit_button.grid(
    row=0,
    column=3,
    padx=5
)

error_label = tk.Label(
    root,
    text="",
    fg="red",
    bg="#eaf4ff",
    font=("Arial", 11, "bold")
)

error_label.pack(pady=5)

current_frame = tk.Frame(
    root,
    bg="white",
    bd=2,
    relief="groove"
)

current_frame.pack(
    fill="x",
    padx=30,
    pady=10
)

city_label = tk.Label(
    current_frame,
    text="Enter a city to see weather",
    font=("Arial", 20, "bold"),
    bg="white"
)

city_label.pack(pady=8)

current_icon_label = tk.Label(
    current_frame,
    bg="white"
)
current_icon_label.pack()

current_weather_label = tk.Label(
    current_frame,
    text="",
    font=("Arial", 12),
    bg="white",
    justify="center"
)
current_weather_label.pack(pady=5)

hourly_title = tk.Label(
    root,
    text="Next 6 Hours",
    font=("Arial", 18, "bold"),
    bg="#eaf4ff"
)
hourly_title.pack(pady=8)

hourly_frame = tk.Frame(
    root,
    bg="#eaf4ff"
)
hourly_frame.pack()

daily_title = tk.Label(
    root,
    text="5-Day Forecast",
    font=("Arial", 18, "bold"),
    bg="#eaf4ff"
)
daily_title.pack(pady=10)

daily_frame = tk.Frame(
    root,
    bg="#eaf4ff"
)
daily_frame.pack()
root.mainloop()
