import tkinter as tk
import random
import pygame

# Initialize pygame mixer for MP3 sound
pygame.mixer.init()

# Dictionary with words as keys and hints as values
word_hints = {
    "RNAse": ["An enzyme that breaks down RNA.", "Commonly used in molecular biology."],
    "Helix": ["A twisted structure, like a spiral staircase.", "Found in DNA and proteins."],
    "Exons": ["Coding regions of genes.", "They are expressed as proteins."],
    "Codon": ["A sequence of three DNA or RNA nucleotides.", "Codes for an amino acid."],
    "Probe": ["Used to detect specific DNA or RNA sequences.", "Important in genetic testing."],
    # Add more words and hints here
}

# Choose a random word from the dictionary
target_word = ""
attempts_left = 5
incorrect_guesses = 0  # Counter for incorrect guesses
hints_given = 0
game_over = False  # Variable to track if the game is over
word_list = list(word_hints.keys())
score = 0
correct_guesses = 0  # Counter for correct guesses

# Load MP3 sound files
correct_sound = pygame.mixer.Sound("Correct.mp3")
incorrect_sound = pygame.mixer.Sound("Incorrect.mp3")

def choose_word():
    global target_word, attempts_left, incorrect_guesses, hints_given, game_over, score, correct_guesses
    if len(word_list) == 0:
        result_label.config(text="Thanks for playing! Come back tomorrow for new words.\n\n"
                                  "1. Correct Guesses: {}/{}\n"
                                  "2. Score: {}/{}".format(correct_guesses, len(word_hints), score, len(word_hints) * 40))
        try_again_button.config(state="disabled")
        next_word_button.config(state="disabled")
        return
    
    target_word = random.choice(word_list)
    word_list.remove(target_word)
    attempts_left = 5
    incorrect_guesses = 0
    hints_given = 0
    game_over = False
    hint_button.config(state="normal")
    result_label.config(text=f"Attempts left: {attempts_left}")
    hint_label.config(text="")
    feedback_label.config(text="")
    feedback_label2.config(text="")
    try_again_button.config(state="disabled")
    next_word_button.config(state="disabled")

def check_guess():
    global attempts_left, incorrect_guesses, hints_given, game_over, score, correct_guesses
    
    if game_over:
        return
    
    guess = guess_entry.get().strip().lower()  # Convert to lowercase and remove leading/trailing whitespace
    target = target_word.lower()  # Convert the target word to lowercase for comparison
    
    if guess == target:
        correct_sound.play()
        score += 40
        correct_guesses += 1
        result_label.config(text=f"Congratulations! You guessed the word: {target_word}\n\n"
                                  "1. Correct Guesses: {}/{}\n"
                                  "2. Score: {}/{}".format(correct_guesses, len(word_hints), score, len(word_hints) * 40))
        game_over = True
        try_again_button.config(state="disabled")
        next_word_button.config(state="normal")
        hint_button.config(state="disabled")
    else:
        incorrect_sound.play()
        attempts_left -= 1
        if attempts_left <= 0:
            result_label.config(text=f"Sorry, you're out of attempts. The word was: {target_word}\n\n"
                                      "1. Correct Guesses: {}/{}\n"
                                      "2. Score: {}/{}".format(correct_guesses, len(word_hints), score, len(word_hints) * 40))
            game_over = True
            try_again_button.config(state="normal")
            next_word_button.config(state="disabled")
            hint_button.config(state="disabled")
        else:
            incorrect_guesses += 1
            if incorrect_guesses == 1 or incorrect_guesses == 3:
                if hints_given < len(word_hints[target_word]):
                    hint_label.config(text=f"Hint: {word_hints[target_word][hints_given]}", fg="blue")
                    hints_given += 1
                else:
                    hint_label.config(text="No more hints available", fg="red")
                hint_button.config(state="normal" if hints_given < len(word_hints[target_word]) else "disabled")
            result_label.config(text=f"Attempts left: {attempts_left}")
            
            # Check for correct and incorrect letters
            correct_letters = []
            incorrect_letters = []
            min_length = min(len(target), len(guess))
            for i in range(min_length):
                if guess[i] == target[i]:
                    correct_letters.append(guess[i])
                elif guess[i] in target and guess[i] not in correct_letters:
                    incorrect_letters.append(guess[i])
            
            feedback_label.config(text=f"Following letters were correctly guessed: {' '.join(correct_letters)}")
            feedback_label2.config(text=f"Letters in the word but in the wrong position: {' '.join(incorrect_letters)}")

def try_again():
    choose_word()

def next_word():
    choose_word()

# Create the main window
root = tk.Tk()
root.title("Bio-Hawords")
root.geometry("800x600")  # Set window dimensions

try:
    root.iconbitmap("icon.ico")  # Set the game icon
except tk.TclError:
    pass  # Icon not found, continue without setting an icon

# Create and place GUI components
word_label = tk.Label(root, text="Guess the Word:", font=("Helvetica", 30))
word_label.pack(pady=20)

guess_entry = tk.Entry(root, font=("Helvetica", 30))
guess_entry.pack()

check_button = tk.Button(root, text="Check", command=check_guess, font=("Helvetica", 24), bg="green", fg="white")
check_button.pack(pady=20)

result_label = tk.Label(root, text=f"Attempts left: {attempts_left}", font=("Helvetica", 24))
result_label.pack()

hint_label = tk.Label(root, text="", font=("Helvetica", 24), fg="blue")
hint_label.pack()

hint_button = tk.Button(root, text="Hint", command=check_guess, font=("Helvetica", 24), state="disabled")
hint_button.pack(pady=20)

# Feedback labels
feedback_label = tk.Label(root, text="", font=("Helvetica", 24))
feedback_label.pack()

feedback_label2 = tk.Label(root, text="", font=("Helvetica", 24))
feedback_label2.pack()

try_again_button = tk.Button(root, text="Try Again", command=try_again, font=("Helvetica", 24), state="disabled")
try_again_button.pack(pady=20)

next_word_button = tk.Button(root, text="Next Word", command=next_word, font=("Helvetica", 24), state="disabled")
next_word_button.pack(pady=20)

choose_word()  # Start the game by choosing the first word

# Start the GUI main loop
root.mainloop()
