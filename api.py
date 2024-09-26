import os
import openai
import time
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPEN_API_KEY")
openai.api_key = API_KEY
client = openai

def run_assistant_api(model, questions):
    assistant = client.beta.assistants.create(model=model, temperature=0)
    thread = client.beta.threads.create()
    message_history = []

    for q in questions:
        start_time = time.time()
        client.beta.threads.messages.create(thread_id=thread.id, role="user", content=q)
        run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response_time = time.time() - start_time
        content = messages.data[0].content[0].text.value
        usage = {
        "completion_tokens": run.usage.completion_tokens,
        "prompt_tokens": run.usage.prompt_tokens,
        "total_tokens": run.usage.total_tokens
        }
        message_history.append({
                "content": content,
                "response_time": f"{response_time:.2f} seconds",
                "usage": usage,
            })
    return message_history

def run_langchain_api(model, questions):
    chat = ChatOpenAI(model=model, temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("placeholder", "{messages}")]
    )
    chain = prompt | chat
    chat_history = ChatMessageHistory()
    message_history = []

    for q in questions:
        start_time = time.time()
        chat_history.add_user_message(q)
        response = chain.invoke({"messages": chat_history.messages})
        chat_history.add_ai_message(response.content)
        response_time = time.time() - start_time
        usage = response.response_metadata['token_usage']

        message_history.append({
                "content": response.content,
                "response_time": response_time,
                "usage": usage
            })
    return message_history  