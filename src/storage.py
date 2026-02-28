import json
import os
from typing import List, Optional
from src.models import UserSession

class StorageManager:
    """
    Manages local persistence of user sessions using JSON.
    """
    def __init__(self, filename: str = "user_history.json"):
        self.filename = filename

    def save_session(self, session: UserSession):
        """Appends the given session to the history file."""
        history = self.load_history()
        history.append(session)
        
        # Serialize all
        data = [s.to_dict() for s in history]
        
        try:
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Session saved to {self.filename}.")
        except Exception as e:
            print(f"Error saving session: {e}")

    def load_history(self) -> List[UserSession]:
        """Loads all past sessions from the history file."""
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [UserSession.from_dict(item) for item in data]
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error loading history: {e}")
            return []
