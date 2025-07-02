Here is the polished README.md content written in plain Markdown, with no unnecessary emoji or symbols:

# Wordle Heuristic Solver

This repository implements a rule-based (heuristic) Wordle solver that guesses words intelligently using letter frequency and position-based scoring — no machine learning required.


---


## Repository Contents

| File                       | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `heuristics_wordle_solver.py` | Main script to run the Wordle solver in interactive or full simulation mode |
| `past_answers.txt`         | Official Wordle solution list used as target words                          |
| `possible_guesses.txt`     | All valid Wordle guesses used for scoring and filtering                     |
| `ai_wordle_solver.ipynb`   | Notebook for experimenting with a future ML-based Wordle solver             |


---


## Features

- Starts with the MIT-recommended word "salet"
- Avoids repeated letters in early guesses when possible
- Filters remaining words based on feedback from all previous guesses
- Interactive mode with Wordle-style feedback (🟩, 🟨, ⬛)
- Simulation mode to compute average guesses and solve rate over all answers
- Uses only built-in Python libraries (no external dependencies)


---


## How to Run

### Step 1: Ensure you have Python 3 installed

### Step 2: Run the script
python heuristics_wordle_solver.py

### Step 3: Select a mode when prompted
1. Guess a random word and show feedback after each guess
2. Run full simulation (average guesses over all solutions)


⸻


Sample Output (Simulation)

Average number of guesses: 3.79
Percentage of words solved in 6 or fewer guesses: 99.09%


⸻


Future Improvements
	•	Add guess distribution visualizations
	•	Implement hard mode constraints
	•	Expand ai_wordle_solver.ipynb with reinforcement learning
