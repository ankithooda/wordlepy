from colorama import Back, Style, Fore
from enum import Enum
import os
import sys
import random

class CharMatchType(Enum):
    FULL_MATCH = 0
    PARTIAL_MATCH = 1
    NO_MATCH = 2

class WordMatch():
    # Should WordMatch do the matching it self, or should there be a separate module
    # which just uses the wordmatch.

    def __init__(self, game_word, user_word):
        self.match = []
        self.done = True
        self._create_match(game_word, user_word)

    def get_match(self, i):
        return self.match[i]

    def _create_match(self, game_word, user_word):
        duplicate_index = {}
        search_result = -1

        for i in range(user_word.length):

            user_char = user_word.get_char(i)

            if user_char in duplicate_index:
                search_result = game_word.search( user_char, duplicate_index[user_char] + 1)
            else:
                search_result = game_word.search( user_char, 0)

            if search_result == -1:
                self.match.append({
                    'value': user_char,
                    'type': CharMatchType.NO_MATCH
                })
                self.done = False
            else:
                duplicate_index[user_char] = search_result
                if search_result == i:
                    self.match.append({
                        'value': user_char,
                        'type': CharMatchType.FULL_MATCH
                    })
                else:
                    self.match.append({
                        'value': user_char,
                        'type': CharMatchType.PARTIAL_MATCH
                    })   
                    self.done = False                 

class Word():

    # Takes a word as string
    def __init__(self, word_string):
        try:
            self.word = self._convert_string_to_array(word_string)
            self.length = len(self.word)
        except TypeError:
            raise Exception("Provide the word as a string object")

    def get_char(self, i):
        return self.word[i]

    def search(self, char, after_index=0):
        try:
            return self.word.index(char.upper(), after_index)
        except ValueError:
            return -1

    def _convert_string_to_array(self, word_string):
        word = []
        for c in word_string.upper():
            word.append(c)
        return word
    

class WordDictionary():
    # How to structure where we need to quicly search for words
    # as well as pick randomly

    def __init__(self, file_location):

        def _create_word_dictionary():
            try:
                file_descriptor = open(file_location)
            except Exception as e:
                print(f"FATAL : Unable to create dictionary due to exception : {e}", file=sys.stderr)
                sys.exit()

            dictionary = []

            for word in file_descriptor.readlines():
                dictionary.append(self._get_clean(word))

            dictionary.sort()    
            return dictionary

        self.dictionary = _create_word_dictionary()

        print(f"Word Dictionary initialized with {len(self.dictionary)} words")

    def get_random_word(self):
        return random.sample(self.dictionary, k=1)[0]

    def exists(self, word):
        return self._get_clean(word) in self.dictionary
        
    def _get_clean(self, word):
        return word.strip().upper()

class WordInput():
    
    def __init__(self, word_length):
        self.word_length = word_length

    def get_input(self):
        word = input()

        if len(word) == self.word_length:
            return word
        else:
            print(f"Word length should be {self.word_length}")
            self.get_input()

class WordMatchOutput():

    def __init__(self, word_length):
        self.word_length = word_length

    def print(self, word_match):
        print("\r", end='')
        for i in range(self.word_length):
            match = word_match.get_match(i)

            if match['type'] == CharMatchType.NO_MATCH:
                print(Fore.WHITE, end='')
                print(Back.RED, end='')
                print(match['value'], end=' ')
                print(Style.RESET_ALL, end='')
            elif match['type'] == CharMatchType.FULL_MATCH:
                print(Fore.WHITE, end='')
                print(Back.GREEN, end='')
                print(match['value'], end=' ')
                print(Style.RESET_ALL, end='')
            elif match['type'] == CharMatchType.PARTIAL_MATCH:
                print(Fore.BLACK, end='')
                print(Back.YELLOW, end='')
                print(match['value'], end=' ')
                print(Style.RESET_ALL, end='')
            else:
                pass
        print()


class WordleGame():

    # Arguments with default values are arranged in order in which they can be customized.
    def __init__(self, tries=6, word_length=5, game_word=None):
        self.tries = tries
        self.word_length = word_length
        self.dictionary = WordDictionary(file_location='words.txt')
        a = self.dictionary.get_random_word()
        print(f"Word is {a}")
        self.game_word = Word(a)
        self.in_driver = WordInput(self.word_length)
        self.out_driver = WordMatchOutput(self.word_length)

    def play_single_try(self):
        word_input = self.in_driver.get_input()

        if self.dictionary.exists(word_input):

            user_word = Word(word_input)

            word_match = WordMatch(self.game_word, user_word)

            self.out_driver.print(word_match)

            if word_match.done:
                print("You Win.")
                sys.exit()
        else:
            print("Enter a valid word.")

    def play(self):
        current_try = 0
        while current_try < self.tries:
            self.play_single_try()
            current_try = current_try + 1
        
        print("You Lose.")
        sys.exit()


        


    



