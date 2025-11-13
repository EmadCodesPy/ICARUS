"""File meant to run as the core connecting the front end and the back end"""
from fastapi import FastAPI
from src.api import app as api_app
from src.model_loader import ModelLoader
from src.chat_manager import ChatManager

app = api_app

models = {'Qwen': 'Qwen/Qwen3-4B-Thinking-2507', 'Mistral': 'mistralai/Mistral-7B-Instruct-v0.3'}

model = ModelLoader(models['Mistral'])
chat_manager = ChatManager()

app.state.model = model
app.state.chat_manager = chat_manager

