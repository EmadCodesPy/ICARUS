"""This file is the component of the main chat page"""
from nicegui import ui
import asyncio

async def typewriter(element: ui.markdown, message: str, delay: float = 0.01):
    element.content = ''
    for char in message:
        element.content += char
        await asyncio.sleep(delay)
        

out = ui.markdown('')
ui.button('Reveal', on_click=lambda: typewriter(out, 'This is your friend, what are you doing right now'))

ui.query('body').style(f'background-color: #ddeeff')
with ui.row().classes(''):
    with ui.card():
        ui.markdown('Hey')

ui.run()