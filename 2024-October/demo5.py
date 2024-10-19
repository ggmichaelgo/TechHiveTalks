import json
import ollama
from googlesearch import search

def google_search(query):
  print("Searching Google: ", query)
  result_list = search(query, num_results=10, advanced=True)
  parsed_results = []

  for result in result_list:
    parsed_results.append({
      "title": result.title,
      "url": result.url,
      "description": result.description
    })

  result = {
    "search_results": parsed_results
  }

  return json.dumps(result)

messages = [
  {"role": "system", "content": "Keep your answer short. You are a bot that can answer questions by using Google search."},
]

def chat(user_input):
  messages.append({"role": "user", "content": user_input})

  response = ollama.chat(
    model="llama3.1",
    messages=messages,
    stream=False,
    tools=[
      {
        "type": "function",
        "function": {
          "name": "google_search",
          "description": "Search Google for information",
          "parameters": {
            "type": "object",
            "properties": {
              "query": {
                "type": "string",
                "description": "The search query",
              },
            },
            "required": ["query"],
          }
        },
      },
    ]
  )

  if response['message']['tool_calls']:
    available_tools = {
      "google_search": google_search
    }

    for tool_call in response['message']['tool_calls']:
      func = tool_call['function']
      func_name = func['name']
      arguments = func['arguments']
      func_result = available_tools[func_name](**arguments)

      messages.append({ "role": "tool", "content": func_result })

  final_response = ollama.chat(
    model="llama3.1",
    messages=messages,
    stream=False
  )

  print(final_response['message']['content'], "\n")

while True:
  user_input = input("User: ")

  if user_input == "exit":
    break

  chat(user_input)