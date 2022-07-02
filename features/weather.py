###########################################################
#------------------------ IMPORTS ------------------------#
###########################################################
import time, requests, config, main

###########################################################
#----------------------- FUNCTIONS -----------------------#
###########################################################
def weather():
    api = f"https://api.openweathermap.org/data/2.5/weather?q={config.LOCAL_CITY}&appid={config.OPEN_WEATHER_MAP_API_KEY}"
    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temperature = int(((json_data['main']['temp'] - 273.15) * 1.8) + 32)
    min_temperature = int(((json_data['main']['temp_min'] - 273.15) * 1.8) + 32)
    max_temperature = int(((json_data['main']['temp_max'] - 273.15) * 1.8) + 32)
    feels_like = int(((json_data['main']['feels_like'] - 273.15) * 1.8) + 32)
    pressure = "{:.2f}".format(float(json_data['main']['pressure'] / 68.948))
    humidity = json_data['main']['humidity']
    wind =  json_data['wind']['speed']
    sunrise = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunrise'] - 18000))
    sunset = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunset'] - 18000))

    print("\n   WEATHER REPORT")
    print("   -------------------------------------------------------------")
    print(f"      LOCATION: {config.LOCAL_CITY}")
    print(f"      CONDITION: {condition}")
    print(f"      TEMPERATURE: {temperature}°F   FEELS LIKE: {feels_like}°F")
    print(f"      MIN TEMP: {min_temperature}°F   MAX TEMP: {max_temperature}°F")
    print(f"      AIR PRESSURE: {pressure} PSI  HUMIDITY: {humidity}%")
    print(f"      WIND SPEED: {wind} MPH")
    print(f"      SUNRISE: {sunrise} AM  SUNSET: {sunset} PM")
    print("   -------------------------------------------------------------")
    main.speak(f"The current weather for {config.LOCAL_CITY} is {condition} with a temperature of {temperature} degrees while it feels like {feels_like} degrees. The current windspeed is {wind} miles per hour.")

