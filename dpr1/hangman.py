"""
Problem Set 2, hangman.py.

Name: Latko Artem
Collaborators: Latko Nazar
Time spent:
----------------------------
Hangman Game
"""
import sys
import random
import string
import os
import logging
import json

WORDLIST_FILENAME = "words.txt"

# the current path to the script
script_path = os.path.dirname(os.path.abspath(__file__))
# change the current working directory to the one where the script is located
os.chdir(script_path)

text_path = os.path.join(script_path, WORDLIST_FILENAME)
config_path = os.path.join(script_path, 'config.json')

with open(config_path, 'r', encoding='utf-8') as config_file:
    config_data = json.load(config_file)

log_level_str = config_data.get('log_level')
log_level = getattr(logging, log_level_str, logging.DEBUG)

# Set up logging based on the configuration
logging.basicConfig(filename=config_data.get('log_file', 'hangman.log'),
                    level=log_level,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')

logger = logging.getLogger(__name__)

if not os.path.exists(text_path):
    logging.fatal("words.txt file not found!!!")
    sys.exit("words.txt file not found!!!")
logging.info("The program is running!")


def load_words():
    """
    Return a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    Wordlist (list): list of words (strings).

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program


wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are lowercase.

    letters_guessed: list (of letters), which letters have been guessed so far;
                     assumes that all letters are lowercase.

    returns: boolean, True if all the letters of secret_word are in letters_guessed;
    False otherwise
    """
    for letter in secret_word:
        if letter not in letters_guessed:
            logging.info(f"The word is guessed: False")
            return False
    logging.info(f"The word is guessed: True")
    return True


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing.

    letters_guessed: list (of letters), which letters have been guessed so far

    returns: string, comprised of letters, underscores (_), and spaces that represents
             which letters in secret_word have been guessed so far.
    """
    letters_of_word = []
    for letter in secret_word:
        if letter not in letters_guessed:
            letters_of_word.append("_ ")
        else:
            letters_of_word.append(letter)
    result_word = ''.join(letters_of_word)
    return result_word


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far.

    returns: string (of letters), comprised of letters that represents which letters have not
             yet been guessed.
    """
    available_letters = []
    for letter in string.ascii_lowercase:
        if letter in letters_guessed:
            continue
        else:
            available_letters.append(letter)
    result_letters = ''.join(available_letters)
    return result_letters


def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    """
    # list for appending guessed letters and conditional data
    letters_guessed = []
    guesses_left = 6
    warn_left = 3

    print("Welcome to the game Hangman!")
    logging.info("Start of the Hangman ")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {warn_left} warnings left.")
    print("-------------")

    while guesses_left > 0:
        print(f"You have {guesses_left} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")

        guess = input(f"Please guess a letter: ").lower()            # enter your guess
        logging.info(f"Guess: {guess}")

        if guess.isalpha() and len(guess) == 1:      # check if guess is letter and len of guess - 1
            if guess in secret_word:
                if guess not in letters_guessed:
                    letters_guessed.append(guess)
                    print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
                    logging.info("The letter is guessed")
                    print("---------------")
                else:
                    logging.error("Incorrect guess!")
                    if warn_left > 0:
                        warn_left -= 1
                        print(f"Oops! You've already guessed that letter. You have {warn_left} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
                        print("---------------")
                    else:
                        guesses_left -= 1
                        print(f"Oops! You've already guessed that letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
                        print("---------------")

                if is_word_guessed(secret_word, letters_guessed):
                    score = guesses_left * len(secret_word)     # the score formula
                    print(f"Congratulations, you won! Your total score for this game is: {score}")
                    logging.info("You won!")
                    logging.info("The program is complete!")
                    break
            else:
                if guess not in letters_guessed:
                    print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")
                    logging.error("Incorrect guess!")
                    print("---------------")
                    letters_guessed.append(guess)
                    if guess in 'aeiou':             # if the vowel is not guessed, then -2 attempts
                        guesses_left -= 2
                    else:                            # if the consonant is not guessed, then -1 attempt
                        guesses_left -= 1
                else:
                    logging.error("Incorrect guess!")
                    warn_left, guesses_left = already_guessed_letter(warn_left, guesses_left, guess, letters_guessed)
        else:
            logging.error("Incorrect guess!")
            warn_left, guesses_left = guess_is_not_letter(warn_left, guesses_left, guess, letters_guessed)

    if guesses_left <= 0:           # lose if there are no attempts left
        print(f"Sorry, you ran out of guesses. The word was {secret_word}")
        logging.info("You lose!")


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word.

    other_word: string, regular English word

    returns: boolean, True if all the actual letters of my_word match the
             corresponding letters of other_word, or the letter is the special symbol
             _ , and my_word and other_word are of the same length;
    False otherwise:
    """
    if len(my_word) != len(other_word):
        return False

    for my_char, other_char in zip(my_word, other_word):
        if my_char != '_' and my_char != other_char:
            return False

    return True


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word.

    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    """
    matching_words = [word for word in wordlist if match_with_gaps(my_word, word)]

    if not matching_words:
        print("No matches found.")
    else:
        print("Possible word matches are: ", end='')
        for matching_word in matching_words:
            print(matching_word, end=' ')
        print("\n---------------")


def already_guessed_letter(warn_left, guesses_left, guess, letters_guessed):
    """
    If already guessed letter.

    Checks to see if there are any warnings left

    If there are no warnings, then the guesses left are subtracted, and if there are,
    then the warnings are subtracted and the guesses left remain unchanged
    """
    if warn_left > 0:              # not all warnings have been used yet
        warn_left -= 1
        print(f"Oops! You've already guessed that letter. You have {warn_left} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
        print("---------------")
    else:              # warnings are all used
        print(f"Oops! You've already guessed that letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
        print("---------------")
        if guess in 'aeiou':          # if the vowel is not guessed, then -2 attempts
            guesses_left -= 2
        else:                         # if the consonant is not guessed, then -1 attempt
            guesses_left -= 1
    return warn_left, guesses_left


def guess_is_not_letter(warn_left, guesses_left, guess, letters_guessed):
    """
    If a guees is not a letter.

    Checks to see if there are any warnings left.

    If there are no warnings, then the guesses left are subtracted, and if there are,
    then the warnings are subtracted and the guesses left remain unchanged
    """
    if warn_left > 0:
        warn_left -= 1
        print(f"Oops! That is not a valid letter. You have {warn_left} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
        print("---------------")
    else:
        print(f"Oops! That is not a valid letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
        print("---------------")
        guesses_left -= 1
    return warn_left, guesses_left


def hangman_with_hints(secret_word, hints=True):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    """
    # list for appending guessed letters and conditional data
    letters_guessed = []
    guesses_left = 6
    warn_left = 3

    print("Welcome to the game Hangman!")
    logging.info("Start of the Hangman ")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {warn_left} warnings left.")
    print("-------------")

    while guesses_left > 0:
        print(f"You have {guesses_left} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        guess = input(f"Please guess a letter: ").lower()            # enter your guess
        logging.debug(f"Guess: {guess}")

        if guess.isalpha() and len(guess) == 1:      # check if guess is letter and len of guess - 1
            if guess in secret_word:
                if guess not in letters_guessed:
                    letters_guessed.append(guess)
                    print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
                    logging.info("The letter is guessed")
                    print("---------------")
                else:
                    logging.error("Incorrect guess!")
                    if warn_left > 0:
                        warn_left -= 1
                        print(f"Oops! You've already guessed that letter. You have {warn_left} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
                        print("---------------")
                    else:
                        guesses_left -= 1
                        print(f"Oops! You've already guessed that letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
                        print("---------------")

                if is_word_guessed(secret_word, letters_guessed):
                    score = guesses_left * len(secret_word)     # the score formula
                    print(f"Congratulations, you won! Your total score for this game is: {score}")
                    logging.info("You won!")
                    logging.info("The program is complete!")
                    break
            else:
                if guess not in letters_guessed:
                    print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")
                    logging.error("Incorrect guess!")
                    print("---------------")
                    letters_guessed.append(guess)
                    if guess in 'aeiou':             # if the vowel is not guessed, then -2 attempts
                        guesses_left -= 2
                    else:                            # if the consonant is not guessed, then -1 attempt
                        guesses_left -= 1
                else:
                    logging.error("Incorrect guess!")
                    warn_left, guesses_left = already_guessed_letter(warn_left, guesses_left, guess, letters_guessed)
        elif guess == '*' and hints is True:                # if we play with hints, when entering * words are displayed that can be a secret word
            show_possible_matches(get_guessed_word(secret_word, letters_guessed).replace(' ', ''))
            logging.info("You used a hint")
        else:
            logging.error("Incorrect guess!")
            warn_left, guesses_left = guess_is_not_letter(warn_left, guesses_left, guess, letters_guessed)

    if guesses_left <= 0:           # lose if there are no attempts left
        print(f"Sorry, you ran out of guesses. The word was {secret_word}")
        logging.info("You lose!")
        logging.info("The program is complete!")


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word, hints=True)
