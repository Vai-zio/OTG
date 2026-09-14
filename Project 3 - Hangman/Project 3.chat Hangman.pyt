import random

# List of words (dictionary)
word_list = ["horse", "python", "computer", "hangman", "elephant"]

# Randomly select a word from the list
word = random.choice(word_list)

# List to keep track of correctly guessed letters
guessed_word = ["_"] * len(word)

# Keep track of guessed letters
guessed_letters = []

# Define number of allowed attempts
attempts = 6  # You can modify the number of allowed guesses

# Game loop - Continue until word is guessed or attempts run out
while attempts > 0 and "_" in guessed_word:
    # Display the current state of the word
    print("\nWord to guess:", " ".join(guessed_word))
    print(f"Guessed letters: {', '.join(guessed_letters)}")
    
    # Ask the user for a guess
    input_letter = input("What is your guess? ").lower()
    
    # Check if the letter was already guessed
    if input_letter in guessed_letters:
        print("You already guessed that letter. Try a different one.")
        continue

    # Add the guessed letter to the list of guessed letters
    guessed_letters.append(input_letter)
    
    # Check if the guessed letter is in the word
    if input_letter in word:
        # If correct, reveal the guessed letter in the correct positions
        for index, letter in enumerate(word):
            if letter == input_letter:
                guessed_word[index] = input_letter
        print(f"Good guess! {input_letter} is in the word.")
    else:
        # If incorrect, decrement the number of attempts
        attempts -= 1
        print(f"Wrong guess! You have {attempts} attempts left.")
    
    # Check if the user has guessed the entire word
    if "_" not in guessed_word:
        print("\nCongratulations! You've guessed the word:", word)
        break
else:
    if "_" in guessed_word:
        print("\nSorry, you've run out of attempts! The word was:", word)
