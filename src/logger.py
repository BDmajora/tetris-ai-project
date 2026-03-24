import json
import os

class TrainingLogger:
    def __init__(self, log_file="training_history.json"):
        self.log_file = log_file

    def log(self, game_num, score, epsilon, optimization_report=None):
        """
        Appends a single game's results and optimization data to the JSON history.
        """
        # Create the data entry for this game
        entry = {
            "game": game_num,
            "score": score,
            "epsilon": round(epsilon, 4),
            "optimization": optimization_report
        }
        
        # Load existing data or start a new list
        data = self._load_data()
        data.append(entry)
        
        # Save back to the file
        try:
            with open(self.log_file, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"--- Error writing to log file: {e} ---")

    def _load_data(self):
        """Internal helper to safely read the JSON file."""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []