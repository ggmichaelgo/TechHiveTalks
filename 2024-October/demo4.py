import json
import ollama

def get_real_time_temperature(city):
  print("Fetching real-time temperature for", city)
  result = {
    "temperature": "21'C"
  }

  return json.dumps(result)

def chat(user_input):
  messages = [
    {"role": "system", "content": "Keep your answer short. You are a bot that can answer weather information."},
    {"role": "user", "content": user_input},
  ]

  response = ollama.chat(
    model="llama3.1",
    messages=messages,
    stream=False,
    tools=[
      {
        "type": "function",
        "function": {
          "name": "get_real_time_temperature",
          "description": "Get the current weather for a city",
          "parameters": {
            "type": "object",
            "properties": {
              "city": {
                "type": "string",
                "description": "The name of the city",
              },
            },
            "required": ["city"],
          }
        },
      },
    ]
  )

  if response['message']['tool_calls']:
    available_tools = {
      "get_real_time_temperature": get_real_time_temperature,
    }

    for tool_call in response['message']['tool_calls']:
      func = tool_call['function']
      func_name = func['name']
      arguments = func['arguments']
      func_result = available_tools[func_name](**arguments)

      messages.append({ "role": "tool", "content": func_result })

  print(messages)
  final_response = ollama.chat(
    model="llama3.1",
    messages=messages,
    stream=False
  )

  print(final_response['message']['content'], "\n")

while True:
  user_input = input("Press enter to start a chat or type 'exit' to quit: ")

  if user_input == "exit":
    break

  chat(user_input)
