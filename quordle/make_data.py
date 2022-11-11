# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 16:58:54 2022

This script is intended to build useful lists for analysis of Quordle, a game 
very similar to Wordle. The list of acceptable words for the game is available
as a .txt from here: 
    https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93
    

@author: Ryan Goetz
@email: ryan.m.goetz@gmail.com
"""

from typing import Union
import numpy as np
import os

# -----------------------------------------------------------------------------
# CUSTOM FUNCTIONS
# -----------------------------------------------------------------------------

@np.vectorize
def translate_5_letter(word_: Union[str, np.ndarray]):
    '''
    A (non-invertible) translator which maps word strings to integers based on the
    presence of letters. The translation turns on the corresponding binary bit of 
    a 26-bit for each letter, for example: 

    ' '     ->  0 = 00000000000000000000000000
    'a'     ->  1 = 00000000000000000000000001
    'b'     ->  2 = 00000000000000000000000010
    'c'     ->  4 = 00000000000000000000000100
    'abc'   ->  7 = 00000000000000000000000111 
    'aaba'  ->  3 = 00000000000000000000000011

    Of course, this means that words containing exactly the same letters are sent
    to the same integer values. For example:

        translate('boom') = translate('bomb')

    : param `word_` : Either a `str` or a numpy array of `str` of 5-letter words

    NOTE: This function is written specifically for translating 5-letter words.

    '''

    A = 0
    for letter in word_:
        A |= 2**(ord(letter)-97) 
    return A


# a vectorized score calculator
def score_calc(word_: Union[str, np.ndarray], weights_: np.ndarray):
    '''
    A function for calculating scores for words based on given weights for each
    letter.
    
    : param `word_` :
    : param `weights_` : 

    '''
    A = translate_5_letter(word_)

    if isinstance(word_, str):
        score = 0
        for idx, weight in enumerate(weights_):
            score += weight*(A & (2**idx))//(2**idx)
    elif isinstance(word_, np.ndarray):
        score = np.zeros_like(A)
        for idx1, a in enumerate(A):
            for idx2, weight in enumerate(weights_):
                score[idx1] += weight*(A & (2**idx2))//(2**idx2)
    return score


# Vectorize ord()
@np.vectorize
def v_ord(character_: str):
    return ord(character_)-97

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------



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

def run():
    # Calculate and save weights to .txt
    WEIGHTS = np.zeros(26,dtype=np.int64)
    with open(WORDLE_PATH(),'r') as f: 
        g = f.read()
        for ind in range(len(g)):
            if ind%6 == 5:
                pass
            else:
                WEIGHTS[ord(g[ind])-97] += 1
    np.savetxt(WEIGHTS_PATH(), WEIGHTS, fmt='%s')

    # Sort the wordle words by score (non-uniques removed) and write to .txt
    with open(WORDLE_PATH(),'r') as f:
        WORDS = np.asarray(f.read().splitlines())

    TRANS = translate_5_letter(WORDS)
    _ , UNIQUES = np.unique(TRANS, return_index = True)
    WORDS = WORDS[UNIQUES]
    SCORES = score_calc(WORDS, WEIGHTS)
    SORTED_WORDS = WORDS[SCORES.argsort()][::-1]
    np.savetxt(WORDS_PATH(), SORTED_WORDS, fmt='%s')

    # Calculate the mask for each letter and write its transpose to .txt
    WORD_MASK = np.ones((26,len(SORTED_WORDS)), dtype=np.int8)
    for idx in range(len(SORTED_WORDS)):
        word = SORTED_WORDS[idx]
        IDXS = v_ord(list(word))
        WORD_MASK[IDXS,idx] = 0
    np.savetxt(MASK_PATH(), WORD_MASK.T,fmt='%s')


    if __name__ == "__main__":

        run()


