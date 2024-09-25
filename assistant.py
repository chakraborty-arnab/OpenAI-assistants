import os
import openai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPEN_API_KEY")
openai.api_key = API_KEY
client = openai

assistant = client.beta.assistants.create(model = "gpt-4o-mini", temperature = 0)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
thread_id = thread.id,
role = "user",
content = "Solve for x in the equation: 3x + 11 = 14")

run = client.beta.threads.runs.create_and_poll(
thread_id = thread.id,
assistant_id=assistant.id)

messages = client.beta.threads.messages.list(
thread_id=thread.id
)

message = client.beta.threads.messages.create(
thread_id = thread.id,
role = "user",
content = "Now get the value of y from the equation y = 2x")

run = client.beta.threads.runs.create_and_poll(
thread_id = thread.id,
assistant_id=assistant.id)

messages = client.beta.threads.messages.list(
thread_id=thread.id
)

for message in messages.data[::-1]:
    role = message.role
    content = message.content[0].text.value
    print(f"{role.capitalize()}: {content}\n")