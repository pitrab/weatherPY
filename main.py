from PIL import Image, ImageTk
import requests
import tkinter as tk
from tkinter import messagebox

def fetch_weather():
    city = city_entry.get().replace(" ", "_")
    api_key = '5d91f9d00707412dbab151716241905'
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        city_name = data['location']['name']
        country = data['location']['country']
        temperature = data['current']['temp_c']
        weather = data['current']['condition']['text']
        icon_url = f"http:{data['current']['condition']['icon']}"

        icon_response = requests.get(icon_url, stream=True)
        icon_response.raise_for_status()  # Ensure the request was successful
        icon_image = Image.open(icon_response.raw).resize((100, 100))
        img = ImageTk.PhotoImage(icon_image)

        weather_label.config(text=f'Country: {country}\nLocation: {city_name}\nTemperature: {temperature}°C\nWeather: {weather}')
        img_label.config(image=img)
        img_label.image = img

    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error', f"Unable to fetch weather data: {e}")
    except KeyError:
        messagebox.showerror('Error', 'Invalid response from the API. Please check the city name.')

root = tk.Tk()
root.title('Weather App')

city_label = tk.Label(root, text='City: ')
city_label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

fetch_button = tk.Button(root, text='Search', command=fetch_weather)
fetch_button.pack()

img_label = tk.Label(root)
img_label.pack()

weather_label = tk.Label(root, text='Weather: ')
weather_label.pack()

root.mainloop()
