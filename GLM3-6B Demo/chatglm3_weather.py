import json
from openai import OpenAI
from weather_function import get_weather, recommend_dress_by_weather, amap_weather_action

client = OpenAI(
    api_key = "xxxx",
    base_url = "http://api.com/v1" #your own url
)

function_map = {
    "get_weather": get_weather
}
def run_conversation():
    MODEL = "chatglm3-6b"
    messages = [
            {"role": "user", "content": "How' the weather like today in Beijing? Do you have any suggestions about clothing?"},
        ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
        functions=[
            {
                "name": "get_weather",
                "description": "Get the current weather and get the weather recommendations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City name for the weather query",
                        },
                    },
                    "required": ["city"],
                }
            }
        ],
        function_call="auto",
    )
    #print(response)
    respone_message = response.choices[0].message
    #print(respone_message)

    if hasattr(respone_message, "function_call"):
        function_call = respone_message.function_call
        function_name = function_call.name
        arguments = json.loads(function_call.arguments)
        #function_to_call = function_mapping.get(SkillFunctions[function_name], lambda **args: "Function not found")
 
        function_response = function_map.get(function_name, lambda **args: "Function not found")(**arguments)
  
        messages.append(respone_message)
        messages.append({
            "role": "function",
            "name": function_name,
            "content": function_response,
        })
    else:
        print("No function call in the response or response_message is None.")
        
    completion_final = client.chat.completions.create(
        model = "chatglm3-6b",
        messages = messages,
    )

    print(completion_final.choices[0].message.content)

run_conversation()
