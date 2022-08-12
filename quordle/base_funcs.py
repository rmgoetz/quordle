# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 22:30:06 2022

@author: Ryan Goetz
@email: ryan.m.goetz@gmail.com
"""

import numpy as np
import os

# a translator that uniquely identifies words, ignoring repeated letters
def translate(word_):
    A = 0
    for letter in word_:
        A |= 2**(ord(letter)-97) 
    return A
translate = np.vectorize(translate)


# a vectorized score calculator
def score_calc(word_):
    A = translate(word_)
    score = 0
    for idx, weight in enumerate(WEIGHTS):
        score += weight*(A & (2**idx))//(2**idx)
    return score
score_calc = np.vectorize(score_calc)


# Vectorize ord()
def v_ord(character):
    return ord(character)-97
v_ord = np.vectorize(v_ord)


# define many paths of importance
def DATA_PATH():
    return os.path.join(os.getcwd(),'word_data')
def WORDLE_PATH():
    return os.path.join(DATA_PATH(),'wordle_words.txt')
def WEIGHTS_PATH():
    return os.path.join(DATA_PATH(), 'wordle_weights.txt')
def WORDS_PATH():
    return os.path.join(DATA_PATH(), 'simple_sorted_wordle_words.txt')
def MASK_PATH():
    return os.path.join(DATA_PATH(), 'wordle_word_mask.txt')