import logging 
import threading 
import time
from sportbook_thread_manager import SportbookThreadManager

class thread_manager:
    def __init__(self) -> None:
        self.sportbook_threads = {"betmgm": None, "bovada": None, "caesars": None, "draftkings": None, "espn": None, "pinnacle": None}
        self.sportbook_thread_manager = SportbookThreadManager()
    def start_threads(self) -> None:
        count = 0
        for key in self.sportbook_threads.keys():
            self.sportbook_threads[key] = threading.Thread(target = self.sportbook_thread_manager.dump_data, args =(key,), daemon=False)
        for key, val in self.sportbook_threads.items():
            val.start()
        for key, val in self.sportbook_threads.items():
            val.join()

