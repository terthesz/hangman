#
# Hangman By: TerThesz
# ! This Was My First Ever Project In Python. Please Dont Judge !
#

import requests
import os
import re

from random import seed
from random import randint

seed(1)

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

url = 'http://api.wordnik.com/v4/words.json/randomWord?hasDictionaryDef=true&includePartOfSpeech=noun&minCorpusCount=8000&maxCorpusCount=-1&minDictionaryCount=3&maxDictionaryCount=-1&minLength=6&maxLength=12&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5'

def get_word():
  r = requests.get(url)
  response = r.json()

  return response['word']

restartGame = True
def start_game():
  global restartGame
  while restartGame:
    clear()
    print('Please Wait. . .')

    word = get_word()
    word_chars = list(word)
    guessed_chars = list('_' * len(word_chars))
    guessed_number_of_chars = 0
    all_guesses = []
    error = None
    errors = [ 'You have already tried this character.', 'You have already used up your hints.' ]
    misses = 0
    won = False
    hints = len(word) // 3
    used_hints = 0

    clear()
    print('Game Started.\nSupported commands while guessing: **restart, stop, hint**.\nYou can have 9 misses (head, torso, arms, legs, eyes and mouth).\n')

    def print_main_line():
      if error != None: print('{one}\n\n{error}\nMisses: {two}/9 | Hints: {three}/{four}     '.format(one = ' '.join(guessed_chars), two = misses, three = used_hints, four = hints, error = errors[error]), end="")
      else: print('{one}\n\nMisses: {two}/9 | Hints: {three}/{four}     '.format(one = ' '.join(guessed_chars), two = misses, three = used_hints, four = hints), end="")

    def clear_lines(lines = 2, err = None):
      if err != None: lines += 1

      print('\033[K\033[A' * lines)

    while misses != 9:
      print_main_line()
      
      raw_guess = input('Your Guess: ')
      while raw_guess is '':
        clear_lines(4, error)

        print_main_line()
        raw_guess = input('Your Guess: ')

      guess = raw_guess[0].lower()

      if raw_guess == 'restart':
        clear()
        break
      elif raw_guess == 'stop': return
      elif raw_guess == 'hint':
        if hints == used_hints:
          clear_lines(4, error)
          error = 1
          continue

        indexes = []
        index = 0
        for i in guessed_chars:
          if i == '_': indexes.append(index)
          index += 1

        guess = word_chars[indexes[randint(0, len(indexes) - 1)]]
        used_hints += 1

      if guess in all_guesses:
        clear_lines(4, error)
        error = 0
        continue
      else: all_guesses.append(guess)
      index = 0
      guesses_incremented = False
      for char in word_chars:
        if char == guess: 
          guessed_chars[index] = char
          guessed_number_of_chars += 1
          guesses_incremented = True

        index += 1
      
      if guessed_number_of_chars == len(word):
        won = True
        break
      elif not guesses_incremented: misses += 1

      clear_lines(4, error)
      error = None

    clear()
    print('The Word Was: ' + word)
    if won: print('\nYou Have Won! Congratulations!')
    else: print('You Have Lost. Better Luck Next Time.')

    decision = None
    while decision is None:
      decision = input('Do you want to play again? [Y/n]: ').lower()
      if decision == 'y' or decision == '': restartGame = True
      elif decision == 'n': restartGame = False
      else:
        clear_lines()
        decision = None

if __name__ == '__main__':
  start_game()