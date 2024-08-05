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
SHEET = GSPREAD_CLIENT.open("hangman_words_list")

def get_words_from_sheet():
    # Get all words from sheet 
    words = SHEET.col_values(1)
    return [word.upper() for word in words if word]

def add_word_to_sheet():
    # Add a new word to the sheet
    SHEET.append_row([word_upper()])

class Hangman:
    def __init__(self, words):
        self.words = words
        self.word_to_guess = random.choice(self, words)
        self.guesses = set()
        self.incorrect_guesses = 0
        self.max_guesses = 6

    








def main():
    print('Welcome to Hangman!')


if __name__ == "__main__":
    main()
