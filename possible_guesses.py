# Import required modules
import requests
import os
# All possible wordle guesses
url = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words" 
response = requests.get(url)
wordlist = response.text.split()
print(f"Total possible guesses: {len(wordlist)}")

# Initialize letter counts
letter_counts = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

# Count letters in the wordlist
for word in wordlist:
    for letter in word:
        if letter in letter_counts:
            letter_counts[letter] += 1

# Sort and Print Letters by frequency
sorted_letters = dict(sorted(letter_counts.items(), key = lambda item: item[1], reverse=True))
print(f"Letter counts: {sorted_letters}")

# Determine the path to the 'data' folder relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "data")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "possible_guesses_data.txt")

# Export sorted letters to a file in the 'data' folder
with open(output_path, "w") as f:
    for letter, count in sorted_letters.items():
        f.write(f"{letter}: {count}\n")

# Save the word list to 'possible_guesses.txt' in the data folder
guesses_path = os.path.join(output_dir, "possible_guesses.txt")
with open(guesses_path, "w") as f:
    for word in wordlist:
        f.write(f"{word}\n")