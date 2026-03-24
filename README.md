# High-Performance Tetris AI and Inference Optimization Pipeline

A high-performance Tetris engine and autonomous AI agent. This project implements a modular systems architecture to handle grid logic, block collisions, and Deep Q-Learning trajectory planning, coupled with a specialized telemetry and optimization suite.

## Features

* **Custom Game Engine:** High-performance Tetris environment built from scratch using Pygame, designed for deterministic AI training cycles.
* **Deep Q-Learning Agent:** Implements a PyTorch-based neural network that evaluates state-space complexity (holes, height, and column disparity) to execute optimal moves in real-time.
* **Inference Optimization (PTQ):** Features a custom Post-Training Quantization pipeline. Using NumPy and Linear Algebra, I manually mapped FP32 weights to INT8 precision, achieving a 75% reduction in parameter memory footprint for edge-deployment readiness.
* **Automated Telemetry and Logging:** Integrated a structured JSON logging system that captures game-by-game performance, epsilon decay, and optimization metrics.
* **Data Visualization:** A built-in Matplotlib analytics engine that automatically generates training reports (progress_report.png) to visualize learning trends and score convergence.

## Technical Stack and Dependencies

This project is built with Python 3.10+ and utilizes the following libraries:

* **PyTorch**: Provides the tensor framework for managing AI parameters, backpropagation, and model state evaluation.
* **Pygame**: Handles high-speed graphical rendering, hardware input, and the primary game loop.
* **NumPy**: Executes low-level linear algebra operations and manual affine quantization math for inference optimization.
* **Matplotlib**: Used for data interpretation and generating visual training reports.
* **Standard Libraries**: Utilizes json for telemetry, copy for state-space simulations, and random for standard Tetris 7-bag generation logic.

## Project Structure

* run.py: Main entry point featuring an automated training and optimization loop.
* src/trainer.py: Neural network architecture and DQN Agent logic.
* src/optimize.py: Quantization scripts for FP32 to INT8 weight conversion.
* src/logger.py: Modular class for handling training history and JSON persistence.
* src/plot_results.py: Analytics suite for generating training performance graphs.

## Performance Tracking

The system automatically tracks training progress in training_history.json. Upon exiting the application, the pipeline triggers a final optimization pass and generates a visual report of the agent's learning curve versus exploration rate.

## Installation

1. Clone the repository:
   git clone https://github.com/BDmajora/tetris-ai-project.git
   cd tetris-ai-project

2. Set up a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

## Usage

Run with the run.py in the root directory:
python3 run.py
