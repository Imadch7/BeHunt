import os
from pathlib import Path

class Find_Dir:
    @staticmethod
    def get_PATH(dir_name='BeHunt'):
        
        start_path = Path.home()
        for root, dirs, files in os.walk(start_path):
            if dir_name in dirs:
                return Path(root) / dir_name
        
        return None