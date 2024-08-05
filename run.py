import random
import os 
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("hangman_words_list").sheet1

def get_words_from_sheet():
    # Get all words from sheet 
    words = SHEET.col_values(1)
    return [word.upper() for word in words if word]

def add_word_to_sheet(word):
    # Add a new word to the sheet
    SHEET.append_row([word_upper()])

class Hangman:
    def __init__(self, words):
        self.words = words
        self.word_to_guess = random.choice(words)
        self.guesses = set()
        self.incorrect_guesses = 0
        self.max_incorrect_guesses = 6

    def display_word(self):
        return ' '.join([letter if letter in self.guesses else '_' for letter in self.word_to_guess])







def main():
    print('Welcome to Hangman!')
    words = get_words_from_sheet()
    game = Hangman(words)
    print(game.display_word())


if __name__ == "__main__":
    main()
