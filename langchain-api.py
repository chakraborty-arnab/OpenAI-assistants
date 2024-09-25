import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

chat = ChatOpenAI(model="gpt-4o-mini",temperature = 0)

prompt = ChatPromptTemplate.from_messages([
        ("placeholder", "{messages}")]
)

chain = prompt | chat

chat_history = ChatMessageHistory()

input1 = "Solve for x in the equation: 3x + 11 = 14"

chat_history.add_user_message(input1)

response = chain.invoke(
    {
        "messages": chat_history.messages,
    }
)

chat_history.add_ai_message(response)

input2 = "Now get the value of y from the equation y = 2x"

chat_history.add_user_message(input2)

response2 = chain.invoke(
    {
        "messages": chat_history.messages,
    }
)

chat_history.add_ai_message(response)

for chat in chat_history.messages:
    if isinstance(chat, HumanMessage):
        role = "User"
    elif isinstance(chat, AIMessage):
        role = "Assistant"
    
    content = chat.content
    print(f"{role}: {content}\n")