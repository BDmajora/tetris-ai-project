import json
import os

class TrainingLogger:
    def __init__(self, log_file="training_history.json"):
        self.log_file = log_file

    def log(self, game_num, score, epsilon, optimization_report=None):
        # Package session telemetry including score, exploration rate, and optimization metrics
        entry = {
            "game": game_num,
            "score": score,
            "epsilon": round(epsilon, 4),
            "optimization": optimization_report
        }
        
        # Retrieve existing telemetry and append new entry
        data = self._load_data()
        data.append(entry)
        
        # Persist updated training history to JSON
        try:
            with open(self.log_file, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Telemetry log error: {e}")

    def _load_data(self):
        # Validate file existence and execute deserialization
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []