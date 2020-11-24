import random
import string
import re
from typing import Dict, List, Union

# define the output, quick summary what the function exactly does

def random_spell_mistake(token_list, p=0.01):   
    """
    
    
    Parameters
    ----------
    token_list : list of strings
        This is the list of tokenized words.
    p : float, optional
        This represents the probability a letter gets exchanged by a random letter. The default is 0.01.

    Returns
    -------
    final_list : list of strings
        list with the modified tokens
    """
    
    letters = string.ascii_lowercase
    final_list = []
    for token in token_list:
        word_list = []
        for letter in token:
            if random.uniform(0,1) < p:
                letter = letters[random.randint(0,len(letters)-1)]
            word_list.append(letter)
            new_word = ''.join(word_list)
        final_list.append(new_word)
    return final_list


neighbours = {
    'q': ['a', 'w'],
    'w': ['q', 'a', 's', 'e'],
    'e': ['w', 's', 'd', 'r'],
    'r': ['e', 'd', 'f', 't'],
    't': ['r', 'f', 'g', 'z'],
    'z': ['t', 'g', 'h', 'u'],
    'u': ['z', 'h', 'j', 'i'],
    'i': ['u', 'j', 'k', 'o'],
    'o': ['i', 'k', 'l', 'p'],
    'p': ['o', 'l'],
    'a': ['q', 'w', 's', 'y'],
    's': ['w', 'e', 'd', 'x', 'y', 'a'],
    'd': ['e', 'r', 'f', 'c', 'x', 's'],
    'f': ['r', 't', 'g', 'v', 'c', 'd'],
    'g': ['t', 'z', 'h', 'b', 'v', 'f'],
    'h': ['z', 'u', 'j', 'n', 'b', 'g'],
    'j': ['u', 'i', 'k', 'm', 'n', 'h'],
    'k': ['i', 'o', 'l', 'm', 'j'],
    'l': ['o', 'p', 'k'],
    'y': ['a', 's', 'x'],
    'x': ['y', 's', 'd', 'c'],
    'c': ['x', 'd', 'f', 'v'],
    'v': ['c', 'f', 'g', 'b'],
    'b': ['v', 'g', 'h', 'n'],
    'n': ['b', 'h', 'j', 'm'],
    'm': ['n', 'j', 'k'],
    ' ': ['c', 'v', 'b', 'n', 'm']
    }


def realistic_spell_mistake(token_list, p = 0.01):
    """
    Parameters
    ----------
    token_list : list of strings
        This is the list of tokenized words.
    p : float, optional
        Probability of exchanging a letter with a neighbour letter. The default is 0.01.

    Returns
    -------
    final_list : list of strings
        list with the modified tokens
    """
    
    final_list = []
    for token in token_list:
        word_list = []
        for letter in token: 
            if random.uniform(0,1) < p:
                if letter.isupper():
                    letter = letter.lower()
                    neighbour_letters = neighbours[letter]
                    letter = neighbour_letters[random.randint(0,len(neighbour_letters)-1)].upper()
                else:
                    neighbour_letters = neighbours[letter]
                    letter = neighbour_letters[random.randint(0,len(neighbour_letters)-1)]
            word_list.append(letter)
            new_word = ''.join(word_list)
        final_list.append(new_word)
    return final_list



def letter_skip(token_list, p=0.01):
    """
    Parameters
    ----------
    token_list : list of strings
        This is the list of tokenized words.
    p : float, optional
        Probability of exchanging a letter with an empty string (i.e. to skip it). The default is 0.01.

    Returns
    -------
    final_list : list of strings
        list with the modified tokens
    """
    
    final_list = []
    for token in token_list:
        word_list = []
        for letter in token:
            if random.uniform(0,1) < p:
                letter = ''
            word_list.append(letter)
            new_word = ''.join(word_list)
        final_list.append(new_word)
    return final_list



def letter_flip(token_list, p=0.01):
    """
    Parameters
    ----------
    token_list : list of strings
        This is the list of tokenized words.
    p : float, optional
        Probability that 2 random (neighbour) letters get switeched the default is 0.01.

    Returns
    -------
    final_list : list of strings
        list with the modified tokens
    """
    
    final_list = []
    for token in token_list:
        word_list = list(token)
        if len(word_list) > 2:
            if random.uniform(0,1) < p:
                idx = random.randint(1,len(word_list)-1)
                word_list[idx], word_list[idx-1] = word_list[idx-1], word_list[idx]
        new_word = ''.join(word_list)
        final_list.append(new_word)
    return final_list


def space_inserter (token_list, p=0.01):
    """
    Inserts random spaces within a word with a certain probability.

    Parameters
    ----------
    token_list : list of strings
        list of tokenized words
    p : float, optional 
        The probability of inserting a random space between two letters. The default is 0.01.

    Returns
    -------
    final_list : list of strings
        modified text

    """
    letters = (" ")
    final_list = []
    for token in token_list:
        word_list = []
        for letter in token:
            if random.uniform(0,1) < p:
                letter = letter + letters
            word_list.append(letter)
            string_word = ''.join(word_list)
        final_list.append(string_word)
    return final_list

def double_letter(token_list, p=0.01):
    """
    Parameters
    ----------
    token_list : list of strings
        This is the list of tokenized words.
    p : float, optional
        Probability that a certain letter occures twice in a row. The default is 0.01.

    Returns
    -------
    final_list : list of strings
        list with modified tokens
    """
    
  final_list = []
  for token in token_list:
      word_list = []
      for letter in token:
          if random.uniform(0,1) < p:
              letter = 2*letter
          word_list.append(letter)
          new_word = ''.join(word_list)
      final_list.append(new_word)
  return final_list
