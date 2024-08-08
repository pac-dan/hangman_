import random
import os
import json
import gspread
from colorama import init, Fore, Style
from google.oauth2.service_account import Credentials

# Initialize colorama
init(autoreset=True)

# Load credentials from environment variable
creds_json = os.getenv('GOOGLE_CREDS_JSON')

CREDS = Credentials.from_service_account_file('creds.json')

SCOPED_CREDS = CREDS.with_scopes([
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
])
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("hangman_words_list").sheet1


def get_words_from_sheet():
    """
    Retrieve all words from the Google Sheets document

    Returns:
        list: A list of words from the Google Sheet,
        converted to uppercase.
    """
    words = SHEET.col_values(1)
    return [word.upper() for word in words if word]


def add_word_to_sheet(word):
    """
    Add a new word to the Google Sheets document.

    Args:
        word(str): The word to add to the Google Sheet.
    """
    SHEET.append_row([word.upper()])


class Hangman:
    """
    A class represents the Hangman game.

    Attributes:
        words(list): A list of words from which the word to guess is
        randomly selected.
        word_to _guess (str): The word that the player has to guess.
        guesses (set): A set of letters and words that the player has guessed.
        incorrect_guesses (int): The count of incorrect guesses made by
        the player.
        max_incorrect_guesses (int): The maximum number of incorrect guesses
        allowed.
    """

    def __init__(self, words):
        """
        Initializes the Hangman game with a list of words.

        Args:
            words (list): A list of words from which the word to guess
            is randomly selected.
        """
        self.words = words
        self.word_to_guess = random.choice(words).upper()
        self.guesses = set()
        self.incorrect_guesses = 0
        self.max_incorrect_guesses = 6

    def display_word(self):
        """
        Displays the current state of the word being guessed.

        Returns:
            str: A string representation of the word using '_' for unguessed
            letters and the correct letters for guessed letters.
        """
        return ' '.join([letter if letter in self.guesses else '_'
                         for letter in self.word_to_guess])

    def make_guess(self, guess):
        """
        Processes the players guess, updating the game state.

        Args:
            guess (str): The players guessed letter or word

        Returns:
            tuple: A tuple containing a boolean indicating whether the guess
            was correct, and a message string with feedback.
        """
        guess = guess.upper()
        if guess in self.guesses:
            return False, Fore.RED + "You already guessed that letter."
        self.guesses.add(guess)
        if len(guess) == 1:
            if guess not in self.word_to_guess:
                self.incorrect_guesses += 1
                return False, Fore.RED + "Incorrect guess."
            return True, Fore.GREEN + "Correct guess."
        elif len(guess) == len(self.word_to_guess):
            if guess == self.word_to_guess:
                self.guesses.update(self.word_to_guess)
                return True, Fore.GREEN 
                "You guessed the whole word correctly!"
            else:
                self.incorrect_guesses += 1
                return False, Fore.RED + "Incorrect guess."
        else:
            return False, Fore.RED + "Invalid guess length, please try again."

    def is_winner(self):
        """
        Checks if the player has guessed the word correctly.

        Returns:
            bool: True if the player has guessed the word correctly,
            False otherwise.
        """
        return all(letter in self.guesses for letter in self.word_to_guess)

    def is_loser(self):
        """
        Checks if the player has reached the maximum number
        of incorrect guesses.

        Returns:
            bool: True if the player has reached the maximum number of
            incorrect guesses, False otherwise.
        """
        return self.incorrect_guesses >= self.max_incorrect_guesses

    def display_hangman(self):
        """
        Displays the current hangman drawing based on the number of
        incorrect guesses.

        Returns:
            str: A string representation of the hangman drawing.
        """
        stages = [
            """
               -----
               |   |
                   |
                   |
                   |
                   |
            """,
            """
               -----
               |   |
               O   |
                   |
                   |
                   |
            """,
            """
               -----
               |   |
               O   |
               |   |
                   |
                   |
            """,
            """
               -----
               |   |
               O   |
              /|   |
                   |
                   |
            """,
            """
               -----
               |   |
               O   |
              /|\\  |
                   |
                   |
            """,
            """
               -----
               |   |
               O   |
              /|\\  |
              /    |
                   |
            """,
            """
               -----
               |   |
               O   |
              /|\\  |
              / \\  |
                   |
            """
        ]
        return stages[self.incorrect_guesses]


def clear_screen():
    """clears the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_instructions():
    """
    Display the Game instructions.
    """
    clear_screen()
    print(Fore.YELLOW + "Welcome to Hangman!")
    print(Fore.YELLOW + "\nInstructions:")
    print(Fore.RED + "1. You need to guess the word by suggesting letters"
          "within a certain number of guesses allowed(6).")
    print(Fore.RED + "2. Each correct letter will be revealed in the word.")
    print(Fore.RED + "3. Each incorrect guess will be added to the Hangman.")
    print(Fore.RED + "4. If you guess the word before the hangman is"
          "fully drawn, you win!")
    print(Fore.RED + "5. If not, you lose. . . ")
    print(Fore.RED + "\nGood Luck and remember to have fun!")
    input(Fore.YELLOW + Style.BRIGHT +
          "\nPress Enter to return to the Main Menu. . .\n")


def play_game():
    """Play one game of hangman"""
    words = get_words_from_sheet()
    game = Hangman(words)

    while True:
        clear_screen()
        print(game.display_hangman())
        print("Word to guess:", game.display_word())
        print(Fore.YELLOW + f"Guesses: {' '.join(sorted(game.guesses))}")
        guess = input(Fore.BLUE +
                      "Enter your guess(word or letter) here:\n"
                      ).strip().upper()

        if not guess.isalpha() or len(guess) == 0:
            print(Fore.RED + "\nInvalid input.Please enter a letter or a word")
            input(Fore.BLUE + "Press Enter To Continue. . .\n")
            continue

        correct, message = game.make_guess(guess)
        print(message)
        input(Fore.BLUE + "Press Enter To Continue. . .\n")

        if game.is_winner():
            print(
                f"Congratulations, you guessed correctly!: "
                f"{game.word_to_guess}\n"
            )
            break

        elif game.is_loser():
            print(
                f"Oh no! You've run out of guesses."
                f"The correct word was: {game.word_to_guess}\n"
            )
            break

    if input(Fore.YELLOW + "Do you want to add a new word to the game?(Y/N):\n"
             ).upper() == 'Y':
        new_word = input(Fore.YELLOW + "Enter new word: \n")
        add_word_to_sheet(new_word)


def main_menu():
    """
    display the main menu and handle user choices
    """

    while True:
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "\nHangman Game")
        print(Fore.GREEN + "1. Play Game")
        print(Fore.GREEN + "2. How to Play")
        print(Fore.RED + "3. Exit")

        choice = input(Fore.BLUE + Style.BRIGHT + "Enter your choice here 1-3:"
                       ).strip()

        if choice == '1':
            clear_screen()
            play_game()
        elif choice == '2':
            display_instructions()
        elif choice == '3':
            print(Fore.GREEN + Style.BRIGHT + "Thanks for playing! Slainte")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter 1, 2 or 3.")
            input(Fore.BLUE + "Press Enter to continue . . .\n")


def main():
    """
    Main function to run the Hangman Game.
    """
    main_menu()


if __name__ == "__main__":
    main()