import random
import string
# import re
# from typing import Dict, List, Union

# define the output, quick summary what the function exactly does

#random_typo
#realistic_typo (with probs and distances or dict)
#letter_skip
#letter_flip
#double_letter
#space_insert

class spell_mistake:
    
    def __init__(self, token_list=None):
        self.token_list = token_list

        self.neighbours = {
            'q': ['a', 'w'],
            'w': ['q', 'a', 's', 'e'],
            'e': ['w', 's', 'd', 'r'],
            'r': ['e', 'd', 'f', 't'],
            't': ['r', 'f', 'g', 'y'],
            'y': ['t', 'g', 'h', 'u'],
            'u': ['y', 'h', 'j', 'i'],
            'i': ['u', 'j', 'k', 'o'],
            'o': ['i', 'k', 'l', 'p'],
            'p': ['o', 'l'],
            'a': ['q', 'w', 's', 'z'],
            's': ['w', 'e', 'd', 'x', 'z', 'a'],
            'd': ['e', 'r', 'f', 'c', 'x', 's'],
            'f': ['r', 't', 'g', 'v', 'c', 'd'],
            'g': ['t', 'y', 'h', 'b', 'v', 'f'],
            'h': ['y', 'u', 'j', 'n', 'b', 'g'],
            'j': ['u', 'i', 'k', 'm', 'n', 'h'],
            'k': ['i', 'o', 'l', 'm', 'j'],
            'l': ['o', 'p', 'k'],
            'z': ['a', 's', 'x'],
            'x': ['z', 's', 'd', 'c'],
            'c': ['x', 'd', 'f', 'v'],
            'v': ['c', 'f', 'g', 'b'],
            'b': ['v', 'g', 'h', 'n'],
            'n': ['b', 'h', 'j', 'm'],
            'm': ['n', 'j', 'k'],
            ' ': ['c', 'v', 'b', 'n', 'm']
            }


        self.keyboard_positions_lower = {
            '`' : (-1,0),
            '1' : (0, 0),
            '2' : (1, 0),
            '3' : (2, 0),
            '4' : (3, 0),
            '5' : (4, 0),
            '6' : (5, 0),
            '7' : (6, 0),
            '8' : (7, 0),
            '9' : (8, 0),
            '0' : (9, 0),
            '-' : (10,0),
            '=' : (11,0),
            
            'q' : (0, 1),
            'w' : (1, 1),
            'e' : (2, 1),
            'r' : (3, 1),
            't' : (4, 1),
            'y' : (5, 1),
            'u' : (6, 1),
            'i' : (7, 1),
            'o' : (8, 1),
            'p' : (9, 1),
            '[' : (10,1),
            ']' : (11,1),
            '\\': (12,1),
            
            'a' : (0, 2),
            's' : (1, 2),
            'd' : (2, 2),
            'f' : (3, 2),
            'g' : (4, 2),
            'h' : (5, 2),
            'j' : (6, 2),
            'k' : (7, 2),
            'l' : (8, 2),
            ';' : (9, 2),
            "'" : (10,2),
            
            
            'z' : (0, 3),
            'x' : (1, 3),
            'c' : (2, 3),
            'v' : (3, 3),
            'b' : (4, 3),
            'n' : (5, 3),
            'm' : (6, 3),
            ',' : (7, 3),
            '.' : (8, 3),
            '/' : (9, 3),
            
            ' ' : (5, 4)
            }
            
        self.keyboard_positions_upper = {
            '~' : (-1,0),
            '!' : (0, 0),
            '@' : (1, 0),
            '#' : (2, 0),
            '$' : (3, 0),
            '%' : (4, 0),
            '^' : (5, 0),
            '&' : (6, 0),
            '*' : (7, 0),
            '(' : (8, 0),
            ')' : (9, 0),
            '_' : (10,0),
            '+' : (11,0),
            
            'Q' : (0, 1),
            'W' : (1, 1),
            'E' : (2, 1),
            'R' : (3, 1),
            'T' : (4, 1),
            'Y' : (5, 1),
            'U' : (6, 1),
            'I' : (7, 1),
            'O' : (8, 1),
            'P' : (9, 1),
            '{' : (10,1),
            '}' : (11,1),
            '|' : (12,1),
            
            'A' : (0, 2),
            'S' : (1, 2),
            'D' : (2, 2),
            'F' : (3, 2),
            'G' : (4, 2),
            'H' : (5, 2),
            'J' : (6, 2),
            'K' : (7, 2),
            'L' : (8, 2),
            ':' : (9, 2),
            '"' : (10,2),
            
            'Z' : (0, 3),
            'X' : (1, 3),
            'C' : (2, 3),
            'V' : (3, 3),
            'B' : (4, 3),
            'N' : (5, 3),
            'M' : (6, 3),
            '<' : (7, 3),
            '>' : (8, 3),
            '?' : (9, 3),
            
            ' ' : (5, 4)
            }

        self.all_chars = [x for x in self.keyboard_positions_upper] + [x for x in self.keyboard_positions_lower]
        print('Andi loaded')

    def random_spell_mistake(self, p=0.01):   
        """
        Inserts random typos with a certain probability.
        
        :param p: This represents the probability a letter gets exchanged by random letter. The default is 0.01.
        :type p: Float
        :yields: List with the modified tokens in List of strings in final_list.
        """
        
        letters = string.ascii_lowercase
        self.final_list = []
        for token in self.token_list:
            word_list = []
            for letter in token:
                if random.uniform(0,1) < p:
                    if letter.isupper():  #optional: with all_chars
                        letter = letters[random.randint(0,len(letters)-1)].upper()
                    else:
                        letter = letters[random.randint(0,len(letters)-1)]         
                word_list.append(letter)
                new_word = ''.join(word_list)
            self.final_list.append(new_word)
        self.token_list=self.final_list
        return self
    
    
    def realistic_spell_mistake(self, p = 0.01):
        """
        Inserts typos based on neighbour keys on a German keyboard with a certain
        probability.
        
        :param p: Probability of echanging a letter with a neighbour letter. The default is 0.01.
        :type p: Float
        :yields: List with the modified tokens in List of strings in final_list.
        """
        
        self.final_list = []
        for token in self.token_list:
            word_list = []
            for letter in token: 
                if random.uniform(0,1) < p:
                    if letter.isupper():
                        letter = letter.lower()
                        neighbour_letters = self.neighbours[letter]
                        letter = neighbour_letters[random.randint(0,len(neighbour_letters)-1)].upper()
                    else:
                        neighbour_letters = self.neighbours[letter]
                        letter = neighbour_letters[random.randint(0,len(neighbour_letters)-1)]
                word_list.append(letter)
                new_word = ''.join(word_list)
            self.final_list.append(new_word)
        self.token_list=self.final_list
        return self
    
    
    
    def letter_skip(self, p=0.01):
        """
        Skips random characters with a certain probability.
        
        :param p: Probabilty of exchanging a letter with an empty string (i.e to skip it). The default is 0.01.
        type p: Float
        :yields: List with the modified tokens in List of strings in final_list.
        """
        
        self.final_list = []
        for token in self.token_list:
            word_list = []
            for letter in token:
                if random.uniform(0,1) < p:
                    letter = ''
                word_list.append(letter)
                new_word = ''.join(word_list)
            self.final_list.append(new_word)
        self.token_list=self.final_list
        return self
    
    
    
    def letter_flip(self, p=0.01):
        """
        Flips two neighbouring characters with a certain probability.
        
        :param p: Probability that 2 random (neighbour) letters get switched. The default is 0.01.
        :type p: Float
        :yields: List with the modified tokens in List of strings in final_list.
        """
        
        self.final_list = []
        for token in self.token_list:
            word_list = list(token)
            if len(word_list) > 2:
                if random.uniform(0,1) < p:
                    idx = random.randint(1,len(word_list)-1)
                    word_list[idx], word_list[idx-1] = word_list[idx-1], word_list[idx]
            new_word = ''.join(word_list)
            self.final_list.append(new_word)
        self.token_list=self.final_list
        return self
    
    
    def space_inserter (self, p=0.01):
        """
        Inserts random spaces in a word with a certain probability.  
        
        :param p: Probability of inserting a random space between two letters. The default is 0.01.
        :type p: Float
        :yields: List with the modified text in List of strings in final_list.
        """
        self.final_list = []
        for token in self.token_list:
            word_list = []
            for letter in token:
                if random.uniform(0,1) < p:
                    letter = letter + ' '
                word_list.append(letter)
                string_word = ''.join(word_list)
            self.final_list.append(string_word)
        self.token_list=self.final_list
        return self
    
    
    def double_letter(self, p=0.01):
        """
        Doubles characters with a certain probability.
        
        :param p: Probabilty that a certain letter occures twice in a row. The default is 0.01 
        :type p : Float
        :yields: List with the modified tokens in List of strings in final_list.
        """
        
        self.final_list = []
        for token in self.token_list:
            word_list = []
            for letter in token:
                if random.uniform(0,1) < p:
                    letter = 2*letter
                word_list.append(letter)
            new_word = ''.join(word_list)
            self.final_list.append(new_word)
        self.token_list=self.final_list
        return self
    
        
    def calculate_distance(self, x1,y1,x2,y2):
        """
        Calculates the euclidean distance between two points in a two-dimensional space.
        
        :param x1: x coordinate of first point
        :type x1: Integer
        :param y1: Y coordinate of first point
        :type y1: Integer
        :param x2: x coordinate of secount point
        :type x2: Integer
        :param y2: y coordinate of secound point
        :type y2: Integer
        :return: Eucledian distance between point x and y.
        """
        xdist = x2-x1
        ydist = y2-y1
        return (xdist**2 + ydist**2)**0.5
    
    
    def calculating_probs(self, key):
        """
        Calculates probabilities for all misspelling options of a letter. The closer
        the keys are to each other, the higher the probability will be.
        
        :param key: a single character
        :type key: String
        :return: keys are the letters, values are the assigned probabilities from either the upper or lower keyboard, depending on the original letter.
        """
        sum_inverse_dists = 0
        inverse_dists = {}
        if key in self.keyboard_positions_lower:
            keyboard_positions = self.keyboard_positions_lower
        else:
            keyboard_positions = self.keyboard_positions_upper
        posx, posy = keyboard_positions[key]
        for letter in keyboard_positions: 
            if letter != key:
                posx1, posy1 = keyboard_positions[letter]
                dist = self.calculate_distance(posx, posy, posx1, posy1)
                inverse_dist = 1/(dist**6)
                inverse_dists[letter] = inverse_dist
                sum_inverse_dists += inverse_dist
        probs = {}
        for key, value in inverse_dists.items():
            probs[key] = value/sum_inverse_dists
        return probs
    
    def pick_random_letter(self, prob_dist):
        """
        Picks a random letter according to the probability distribution from
        calculating_probs.
        
        :param prob_dist: The return from calculating_probs, keys are letters, values are probabilities.
        :type prob_list: Dictionary
        :return: A random letter accoring to the probability dictionary, picked through random choices.
        """
        letters = []
        probs = []
        for key, value in prob_dist.items():
            letters.append(key)
            probs.append(value)
        picked_letter = random.choices(letters, probs)
        return picked_letter[0]
        
        
    def realistic_spell_mistake_with_probs(self, p = 0.01):
        """
        Inserts typos based on a probability distribution calculated based on the
        keyboard distances.
        
        :param p: Probability of altering a single letter. The default is 0.01.
        :type p: Float
        :yields: List of altered strings or tokens in List of Strings in final_list.
        """
        self.final_list = []
        for token in self.token_list:
            word_list = []
            for letter in token: 
                if random.uniform(0,1) < p:
                    neighbour_probs = self.calculating_probs(letter)
                    letter = self.pick_random_letter(neighbour_probs)
                word_list.append(letter)
                new_word = ''.join(word_list)
            self.final_list.append(new_word)
        self.token_list=self.final_list
        return self