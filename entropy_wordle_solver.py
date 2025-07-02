from collections import Counter
import concurrent.futures
import matplotlib.pyplot as plt
import random
import math
import os

# Returns a list of 5 Counter objects, each counting the occurrences of letters at that position.
def letter_frequency(word_list):
    pos_frequency = [Counter() for _ in range(5)]
    for word in word_list:
        for i, c in enumerate(word):
            pos_frequency[i][c] += 1
    return pos_frequency

# Simulate Wordle-style feedback
def get_feedback(guess, answer):
    """
    Returns a list of feedback characters:
    '🟩' = green (correct letter, correct position)
    '🟨' = yellow (correct letter, wrong position)
    '⬛' = black/gray (letter not in word)
    """
    feedback = ['⬛'] * 5
    used = [False] * 5

    # First pass: check for greens
    for i in range(5):
        if guess[i] == answer[i]:
            feedback[i] = '🟩'
            used[i] = True

    # Second pass: check for yellows (correct letter, wrong position)
    for i in range(5):
        if feedback[i] == '⬛': # Initialize all feedback as black
            for j in range(5):  # Track used letters in answer for yellows
                if guess[i] == answer[j] and not used[j] and guess[j] != answer[j]:
                    feedback[i] = '🟨'
                    used[j] = True
                    break

    return feedback

# Returns True if the word contains any repeated letters
def has_repeated_letters(word):
    return len(set(word)) < len(word)


def calculate_entropy(possible_words, guess_list):
    entropy_scores = []
    for guess in guess_list:
        feedback_buckets = {}
        for target in possible_words:
            feedback = tuple(get_feedback(guess, target))
            feedback_buckets[feedback] = feedback_buckets.get(feedback, 0) + 1

        total = len(possible_words)
        entropy = 0.0
        for count in feedback_buckets.values():
            p = count / total
            entropy -= p * math.log2(p)
        entropy_scores.append((guess, entropy))
    entropy_scores.sort(key=lambda x: x[1], reverse=True)
    return entropy_scores

def score_entropy(word_and_solutions):
    word, solutions = word_and_solutions
    return (word, calculate_entropy(solutions, [word])[0][1])

# Extracted entropy scoring logic into a new function
def train_entropy_scores(guesses, solutions):
    print("Training entropy-based model across all guesses (parallelized)...")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(score_entropy, [(w, solutions) for w in guesses]))
    print("Training complete.\n")
    return dict(results)

def run_mode_3(solutions, entropy_scores_map):
    # Mode 1: Interactive single game with random target word
    word = random.choice(solutions)
    remaining_words = solutions.copy()
    num_guesses = 0
    guessed_words = set()

    # First guess is always "salet" according to MIT https://mitsloan.mit.edu/ideas-made-to-matter/how-algorithm-solves-wordle
    guess = "salet"
    guessed_words.add(guess)
    print(f"Guess {num_guesses + 1}: {guess}")
    feedback = get_feedback(guess, word)
    print("Feedback:", feedback)
    num_guesses += 1

    if guess == word:
        print(f"Solved in {num_guesses} guess!")
        return
    
    # Filter out impossible words based on feedback
    remaining_words = [w for w in remaining_words if get_feedback(guess, w) == feedback]

    while True:
        word_scores = [(w, entropy_scores_map[w]) for w in remaining_words if w in entropy_scores_map]
        word_scores.sort(key=lambda x: x[1], reverse=True)

        # Guesses have no repeated letters if possible
        filtered = [w for w, _ in word_scores if not has_repeated_letters(w)]
        if filtered:
            guess = filtered[0]
        else:
            guess = word_scores[0][0]

        guessed_words.add(guess)
        num_guesses += 1
        print(f"Guess {num_guesses}: {guess}")
        feedback = get_feedback(guess, word)
        print("Feedback:", feedback)

        if guess == word:
            print(f"Solved in {num_guesses} guesses!")
            break

        # Narrow down possible answers using all guess history
        remaining_words = [w for w in remaining_words if get_feedback(guess, w) == feedback]

        if num_guesses >= 6:
            print("Failed to solve in 6 guesses.")
            break

def run_mode_2(solutions, entropy_scores_map):
    # Mode 2: Full simulation over all possible solution words
    total_guesses = 0
    solved_in_six_or_less = 0
    all_guess_counts = []

    # Try solving each target word
    for word in solutions:
        remaining_words = solutions.copy()
        num_guesses = 0
        guessed_words = set()

        # First guess is always "salet" according to MIT https://mitsloan.mit.edu/ideas-made-to-matter/how-algorithm-solves-wordle
        guess = "salet"
        guessed_words.add(guess)
        num_guesses += 1
        if guess == word:
            total_guesses += num_guesses
            solved_in_six_or_less += 1
            all_guess_counts.append(num_guesses)
            continue

        # Narrow the word list based on feedback
        feedback = get_feedback(guess, word)
        remaining_words = [w for w in remaining_words if get_feedback(guess, w) == feedback]

        # Continue making guesses until the word is found
        while True:
            word_scores = [(w, entropy_scores_map[w]) for w in remaining_words if w in entropy_scores_map]
            word_scores.sort(key=lambda x: x[1], reverse=True)

            
            # Avoids repeating letters in early guesses if possible
            """
            Adding this heuristic lowered the average number of guesses from 3.81 to 3.79
            Adding this heuristic also decreased the percentage of words solved in 6 or fewer guesses from 99.27% to 99.09%
            """
            filtered = [w for w, _ in word_scores if not has_repeated_letters(w)]
            if filtered:
                guess = filtered[0]
            else:
                guess = word_scores[0][0]

            guessed_words.add(guess)
            num_guesses += 1
            if guess == word:
                break

            # Get feedback and filter again
            feedback = get_feedback(guess, word)
            remaining_words = [w for w in remaining_words if get_feedback(guess, w) == feedback]

            if num_guesses >= 6:
                break

        all_guess_counts.append(num_guesses)
        total_guesses += num_guesses
        if num_guesses <= 6:
            solved_in_six_or_less += 1

    # Print results of full simulation
    average_guesses = total_guesses / len(solutions)
    success_rate = (solved_in_six_or_less / len(solutions)) * 100
    print(f"Average number of guesses: {average_guesses:.2f}")
    print(f"Percentage of words solved in 6 or fewer guesses: {success_rate:.2f}%")

    # Plot histogram of number of guesses
    plt.figure()
    plt.hist(all_guess_counts, bins=range(1, 8), align='left', rwidth=0.8, color='skyblue', edgecolor='black')
    plt.xticks(range(1, 7))
    plt.xlabel("Number of Guesses")
    plt.ylabel("Number of Words Solved")
    plt.title("Distribution of Guesses Needed to Solve Wordle")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def run_mode_4(solutions, guesses, entropy_scores_map):
    # Mode 3: User steps through guesses interactively with suggestions
    word = random.choice(solutions)
    remaining_words = solutions.copy()
    num_guesses = 0
    guessed_words = set()

    while True:
        if num_guesses == 0:
            suggested = "salet"
        else:
            word_scores = [(w, entropy_scores_map[w]) for w in remaining_words if w in entropy_scores_map]
            word_scores.sort(key=lambda x: x[1], reverse=True)
            if not word_scores:
                print("No more words to suggest — remaining_words is empty.")
                break
            filtered = [w for w, _ in word_scores if not has_repeated_letters(w)]
            if filtered:
                suggested = filtered[0]
            else:
                suggested = word_scores[0][0]

        print(f"Suggested guess: {suggested}")

        guess = input("Enter your guess (must be in valid guesses list): ").strip().lower()
        while guess not in guesses:
            guess = input("Invalid guess. Try again: ").strip().lower()

        guessed_words.add(guess)
        num_guesses += 1
        feedback = get_feedback(guess, word)
        print("Feedback:", feedback)

        if guess == word:
            print(f"Solved in {num_guesses} guesses!")
            break

        remaining_words = [w for w in remaining_words if get_feedback(guess, w) == feedback]

        if num_guesses >= 6:
            print("Failed to solve in 6 guesses.")
            break

def run_mode_1(guesses, entropy_scores_map):
    remaining_words = guesses.copy()
    num_guesses = 0
    guessed_words = set()

    while True:
        # Select suggestion based on entropy score
        word_scores = [(w, entropy_scores_map[w]) for w in remaining_words if w in entropy_scores_map]
        word_scores.sort(key=lambda x: x[1], reverse=True)

        filtered = [w for w, _ in word_scores if not has_repeated_letters(w)]
        if num_guesses == 0:
            suggested = "salet"
        elif filtered:
            suggested = filtered[0]
        else:
            suggested = word_scores[0][0]

        print(f"Suggested guess: {suggested}")

        guess = input("Enter the word you guessed (must be in valid guesses list): ").strip().lower()
        while guess not in guesses:
            guess = input("Invalid guess. Try again: ").strip().lower()

        guessed_words.add(guess)
        num_guesses += 1

        raw_feedback = input("Enter feedback (comma-separated; use 'g' for green, 'y' for yellow, anything else for gray): ").strip().lower()
        feedback_parts = [part.strip() for part in raw_feedback.split(',')]
        feedback = []
        for part in feedback_parts:
            if part == 'g':
                feedback.append('🟩')
            elif part == 'y':
                feedback.append('🟨')
            else:
                feedback.append('⬛')
        if len(feedback) != 5:
            print("Invalid feedback length. Must be 5 comma-separated values. Try again.")
            continue

        print("Interpreted Feedback:", feedback)

        if feedback == ['🟩'] * 5:
            print(f"Solved in {num_guesses} guesses!")
            break

        remaining_words = [w for w in remaining_words if get_feedback(guess, w) == feedback]

        if num_guesses >= 6:
            print("Failed to solve in 6 guesses.")
            break

def load_word_lists(data_dir):
    with open(os.path.join(data_dir, 'past_answers.txt')) as f:
        solutions = [line.strip() for line in f]
    with open(os.path.join(data_dir, 'possible_guesses.txt')) as f:
        guesses = [line.strip() for line in f]
    return solutions, guesses

if __name__ == "__main__":
    # Define the path to the 'data' folder relative to the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")

    solutions, guesses = load_word_lists(data_dir)

    # Generate positional frequency table from guess list
    pos_freq = letter_frequency(guesses)

    entropy_scores_map = train_entropy_scores(guesses, solutions)

    while True:
        print("\nChoose a mode:")
        print("1. Suggest guess and take feedback manually")
        print("2. Run full simulation (average guesses over all solutions)")
        print("3. Guess a random word and show feedback after each guess")
        print("4. Manual guessing with suggestions and feedback")
        print("Type 'exit' to quit.")
        mode = input("Enter 1, 2, 3, 4 or 'exit': ").strip().lower()

        if mode == "1":
            run_mode_1(guesses, entropy_scores_map)
        elif mode == "2":
            run_mode_2(solutions, entropy_scores_map)
        elif mode == "3":
            run_mode_3(solutions, entropy_scores_map)
        elif mode == "4":
            run_mode_4(solutions, guesses, entropy_scores_map)
        elif mode == "exit":
            break
        else:
            print("Invalid option. Please try again.")