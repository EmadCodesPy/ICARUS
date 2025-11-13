"""This module is for creating all the backend API logic"""
from fastapi import FastAPI, Request
from fastapi.concurrency import run_in_threadpool
import asyncio
from pydantic import BaseModel
from .chat_manager import ChatManager

app = FastAPI()

chat_manager = ChatManager()

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

@app.post('/chat/{chat_id}/send')
async def send_message(chat_id: int, request: Request):
    #Get JSON data and message
    data = await request.json()
    message = data.get('message')
    #Load the model and chat_managr from the app
    model = request.app.state.model
    chat_manager = request.app.state.chat_manager
    #Send message to model and save it to db
    try:
        chat_manager.add_new_message(chat_id=chat_id, role='user', content=message)
        response = await run_in_threadpool(model.generate, message)
        chat_manager.add_new_message(chat_id=chat_id, role='assistant', content=response)
        return {'success': f'messages added to chat with id {chat_id}', 'response': response}
    except Exception as e:
        return {'error': f'exception raised ({e})'}
    

@app.delete('/chat')
def delete_chat(chat_id: int):
    try:
        chat_manager.delete_chat(chat_id)
        return {'success': f'deleted chat with id {chat_id}'}
    except Exception as e:
        return {'error': f'exception raised ({e})'}