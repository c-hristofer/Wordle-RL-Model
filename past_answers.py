import requests
# All possible wordle guesses
url = "https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/c46f451920d5cf6326d550fb2d6abb1642717852/wordle-answers-alphabetical.txt" 
response = requests.get(url)
wordlist = response.text.split()
print(f"Total past answers: {len(wordlist)}")

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

# Export sorted letters to a file
with open("past_answers_data.txt", "w") as f:
    for letter, count in sorted_letters.items():
        f.write(f"{letter}: {count}\n")