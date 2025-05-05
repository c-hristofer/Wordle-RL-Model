from collections import Counter

# Returns a list of 5 Counter objects, each counting the occurrences of letters at that position.
def letter_frequency(word_list):
    pos_frequency = [Counter() for _ in range(5)]
    for word in word_list:
        for i, c in enumerate(word):
            pos_frequency[i][c] += 1
    return pos_frequency

# Assigns a heuristic score to a word by summing the frequency of its letters at their respective positions.
def score_word(word, pos_freq):
    return sum(pos_freq[i][c] for i, c in enumerate(word))

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

def main():
    # Load Wordle solution and guess word lists
    with open('past_answers.txt') as f:
        solutions = [line.strip() for line in f]

    with open('possible_guesses.txt') as f:
        guesses = [line.strip() for line in f]

    # Generate positional frequency table from guess list
    pos_freq = letter_frequency(guesses)

    # Allow user to choose between interactive single word or full simulation
    print("Choose a mode:")
    print("1. Guess a random word and show feedback after each guess")
    print("2. Run full simulation (average guesses over all solutions)")
    mode = input("Enter 1 or 2: ").strip()

    if mode == "1":
        # Mode 1: Interactive single game with random target word
        import random
        word = random.choice(solutions)
        remaining_words = solutions.copy()
        num_guesses = 0

        # First guess is always "salet" according to MIT https://mitsloan.mit.edu/ideas-made-to-matter/how-algorithm-solves-wordle
        guess = "salet"
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
            # Score remaining words based on heuristic frequency model
            word_scores = [(word, score_word(word, pos_freq)) for word in remaining_words]
            word_scores.sort(key=lambda x: x[1], reverse=True)

            # Guesses have no repeated letters if possible
            filtered = [w for w, _ in word_scores if not has_repeated_letters(w)]
            if filtered:
                guess = filtered[0]
            else:
                guess = word_scores[0][0]

            num_guesses += 1
            print(f"Guess {num_guesses}: {guess}")
            feedback = get_feedback(guess, word)
            print("Feedback:", feedback)

            if guess == word:
                print(f"Solved in {num_guesses} guesses!")
                break

            # Narrow down possible answers using all guess history
            remaining_words = [w for w in remaining_words if get_feedback(guess, w) == feedback]

    else:
        # Mode 2: Full simulation over all possible solution words
        total_guesses = 0
        solved_in_six_or_less = 0

        # Try solving each target word
        for word in solutions:
            remaining_words = solutions.copy()
            num_guesses = 0

            # First guess is always "salet" according to MIT https://mitsloan.mit.edu/ideas-made-to-matter/how-algorithm-solves-wordle
            guess = "salet"
            num_guesses += 1
            if guess == word:
                total_guesses += num_guesses
                solved_in_six_or_less += 1
                continue

            # Narrow the word list based on feedback
            feedback = get_feedback(guess, word)
            remaining_words = [w for w in remaining_words if get_feedback(guess, w) == feedback]

            # Continue making guesses until the word is found
            while True:
                word_scores = [(word, score_word(word, pos_freq)) for word in remaining_words]
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

                num_guesses += 1
                if guess == word:
                    break

                # Get feedback and filter again
                feedback = get_feedback(guess, word)
                remaining_words = [w for w in remaining_words if get_feedback(guess, w) == feedback]

            total_guesses += num_guesses
            if num_guesses <= 6:
                solved_in_six_or_less += 1

        # Print results of full simulation
        average_guesses = total_guesses / len(solutions)
        success_rate = (solved_in_six_or_less / len(solutions)) * 100
        print(f"Average number of guesses: {average_guesses:.2f}")
        print(f"Percentage of words solved in 6 or fewer guesses: {success_rate:.2f}%")

if __name__ == "__main__":
    main()
