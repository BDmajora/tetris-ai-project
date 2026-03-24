import json
import matplotlib.pyplot as plt

def generate_graphs():
    # Load training history and extract session metrics
    with open("training_history.json", "r") as f:
        data = json.load(f)
    
    games = [entry["game"] for entry in data]
    scores = [entry["score"] for entry in data]
    epsilons = [entry["epsilon"] for entry in data]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Primary axis: Performance score visualization
    color = 'tab:blue'
    ax1.set_xlabel('Game Number')
    ax1.set_ylabel('Score', color=color)
    ax1.plot(games, scores, color=color, label="Score")
    ax1.tick_params(axis='y', labelcolor=color)

    # Secondary axis: Exploration rate (Epsilon) decay visualization
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Epsilon (Exploration)', color=color)
    ax2.plot(games, epsilons, color=color, linestyle='--', label="Epsilon")
    ax2.tick_params(axis='y', labelcolor=color)

    # Graph formatting and local persistence
    plt.title('Tetris AI Training Progress')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.savefig("progress_report.png")
    print("Analytics report generated: progress_report.png")
    plt.show()

if __name__ == "__main__":
    generate_graphs()