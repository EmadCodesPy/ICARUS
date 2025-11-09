"""This module is meant to handle the chats between the user and the model"""
from .db_manager import DatabaseManager
from typing import Dict, List
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


class ChatManager():
    
    def __init__(self) -> None:
        """Initialize the Chat Manager using the DatabaseManager class"""
        self.db = DatabaseManager()
    
    def add_new_chat(self, name: str) -> None:
        """Adds new chat to the database
        :param name: The name of your new chat
        """
        with self.db.get_connection() as conn:
            c = conn.cursor()
            c.execute('INSERT INTO chats (name) VALUES (?)', (name,))
            logger.info(f'New chat ({name}) added')
    
    def get_all_chat_ids(self) -> list:
        """Gets all the chat ids, mainly used for validation
        :return : A list of all the existing chat ids
        """
        with self.db.get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM chats')
            rows = c.fetchall()
            return [row[0] for row in rows]
    
    def add_new_message(self, chat_id: int, role: str, content: str) -> None:
        """Saves a message to the database
        :param chat_id: The chat id of the current chat, will raise value error if it doesn't exist
        :param role: The role of the message, e.g. 'user' or 'assistant
        :param content: The content that you would like to add to the database
        """
        with self.db.get_connection() as conn:
            c = conn.cursor()
            all_chat_ids = self.get_all_chat_ids()
            if chat_id not in all_chat_ids:
                raise ValueError(f'Chat id {chat_id} does not exist')
            c.execute('INSERT INTO messages (chat_id, role, content) VALUES (?,?,?)', (chat_id, role, content))
            c.execute('UPDATE chats SET last_updated_at = CURRENT_TIMESTAMP WHERE id = ?', (chat_id,))
    
    def get_chat_messages(self, chat_id: int) -> List[Dict[str,str]]:
        with self.db.get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT role, content FROM messages WHERE chat_id=? ORDER BY timestamp ASC', (chat_id,))
            rows = c.fetchall()
            lst = []
            for row in rows:
                _dict = {'role': row[0], 'content': row[1]}
                lst.append(_dict)
            return lst
    
    def get_all_chat_names_and_ids(self) -> List[Dict[str,str]]:
        with self.db.get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT id, name FROM chats ORDER BY last_updated_at DESC')
            rows = c.fetchall()
            lst = []
            for row in rows:
                _dict = {'id': row[0], 'name': row[1]}
                lst.append(_dict)
            return lst
    
    def delete_chat(self, chat_id: int) -> None:
        with self.db.get_connection() as conn:
            c = conn.cursor()
            all_ids = self.get_all_chat_ids()
            if chat_id not in all_ids:
                raise ValueError(f'Chat id {chat_id} does not exist')
            c.execute('DELETE FROM chats WHERE id=?', (chat_id,))
        logger.info(f'Deleted chat with id: {chat_id}')

if __name__ == '__main__':
    test = ChatManager()
    test.add_new_chat('test')
    test.add_new_message(1,'user','Hello world!')