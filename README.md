# Tetris AI Project

A high-performance Tetris Pygame and AI Tetris agent. This project implements a modular systems architecture to handle grid logic, block collisions, and heuristic-based move planning.

## Features
* **Custom Game Engine:** Built from scratch using Pygame.
* **Heuristic AI:** Real-time move evaluation and pathfinding.
* **Modular Architecture:** Logic decoupled into specialized modules for grid management, positioning, and movement execution.
* **Inference Optimization:** Implements Post-Training Quantization (PTQ) using PyTorch and NumPy to compress heuristic weights from FP32 to INT8, achieving a 75% reduction in parameter memory footprint.

## Dependencies

This project is built with Python 3.10+ and utilizes the following libraries:

* **Pygame**: Handles the graphical rendering, input handling, and the core game loop.
* **PyTorch**: Provides the tensor framework for managing AI parameters and evaluating model states.
* **NumPy**: Executes low-level linear algebra operations and manual affine quantization math for inference optimization.
* **Copy**: Standard library used for state-space deep copies during AI trajectory planning.
* **Random**: Manages randomized block generation following the standard Tetris 7-bag system logic.

## Installation

1. Clone the repository:
   git clone https://github.com/your-username/tetris-ai-project.git
   cd tetris-ai-project

2. Set up a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

## Usage

Run with the run.py in the root directory:
python3 run.py