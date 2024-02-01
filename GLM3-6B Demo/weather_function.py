import json
import requests

def amap_weather_action(city: str) -> dict:
    url = "xxx" #your weather api url
    key = "xxx" #your own weather api key
    params = {
        "city": city,
        "key": key,
        "extensions": "base",
        "output": "JSON"
    }
    #I use amap api initially, buy your can change the params according the document of api.

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] == '1' and data.get("lives"):
            weather_info = data["lives"][0]
            return {
                "temperature": weather_info["temperature"],
                "weather": weather_info["weather"],
                "windpower": weather_info["windpower"]
            }
        else:
            return {"error": "cannot find weather information。"}
    except requests.RequestException as e:
        return {"error": f"request error：{e}"}
    
def recommend_dress_by_weather(temp):
    temp = float(temp)
    if temp < 10:
        return "Thick jacket or down jacket."
    elif 10 <= temp < 20:
        return "Long-sleeved shirt with light jacket."
    elif 20 <= temp < 30:
        return "Short-sleeved T-shirt or blouse."
    else:
        return "Summer clothing, such as shorts and short-sleeved shirts."

def get_weather(city):
    weather_info = amap_weather_action(city)
    if "error" in weather_info:
        return weather_info["error"]
    dress_advice = recommend_dress_by_weather(weather_info["temperature"])
    result = f"The weather of {city} is：{weather_info['weather']}，temperature is：{weather_info['temperature']}°C。\n I recommend you to wear：{dress_advice}"
    return result


