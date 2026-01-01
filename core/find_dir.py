import os
from pathlib import Path

class Find_Dir:
    @staticmethod
    def get_PATH(dir_name='BeHunt'):
        # First, try to find the directory in common locations (avoid Trash)
        preferred_locations = [
            Path.home() / "Desktop",
            Path.home() / "Projects",
            Path.home(),
        ]
        
        for location in preferred_locations:
            target = location / dir_name
            if target.exists() and target.is_dir():
                return target
        
        # Fallback: walk the home directory, but skip Trash
        start_path = Path.home()
        for root, dirs, files in os.walk(start_path):
            # Skip trash and other system directories
            if '.local/share/Trash' in root or '.cache' in root:
                continue
            if dir_name in dirs:
                return Path(root) / dir_name
        
        return None