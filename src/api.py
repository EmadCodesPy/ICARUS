"""This module is for creating all the backend API logic"""
from fastapi import FastAPI
from pydantic import BaseModel
from .chat_manager import ChatManager

app = FastAPI()

users = []

chat_manager = ChatManager()
#Need to make classes. One for the message, one for a chat

class Chat(BaseModel):
    name: str

class Message(BaseModel):
    chat_id: int
    role: str
    content: str

@app.get('/chat/{chat_id}')
def get_messages(chat_id: int):
    messages = chat_manager.get_chat_messages(chat_id)
    return messages

@app.get('/chat')
def get_all_chats():
    all_chats = chat_manager.get_all_chat_names_and_ids()
    return all_chats

@app.post('/chat')
def add_new_chat(chat: Chat):
    chat_manager.add_new_chat(chat.name)
    return {'sucess': f'added chat ({chat.name})'}

@app.post('/chat/{chat_id}')
def add_new_message(message: Message):
    try:
        chat_manager.add_new_message(chat_id=message.chat_id, role=message.role, content=message.content)
        return {'sucess': f'message added to chat with id {message.chat_id}'}
    except Exception as e:
        return {'error': f'exception raised ({e})'}

@app.delete('/chat')
def delete_chat(chat_id: int):
    try:
        chat_manager.delete_chat(chat_id)
        return {'success': f'deleted chat with id {chat_id}'}
    except Exception as e:
        return {'error': f'exception raised ({e})'}