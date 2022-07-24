# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 16:58:54 2022

This script is intended to build useful lists for analysis of Quordle, a game 
very similar to Wordle. The list of acceptable words for the game is available
as a .txt from here: 
    https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93
    
    
    
    
    
IMPORTANT NOTE:
    
CURRENTLY, WORDS ARE DISCARDED BASED ON WHETHER THEY HAVE A DUPLICATE SCORE,
NOT BASED ON THE UNIQUENESS OF THEIR LETTER COMBINATIONS. THIS PRESENTS A
POTENTIAL PROBLEM, AS IT IS POSSIBLE FOR WORDS TO SHARE A SCORE BUT NOT A
MASK.

FOR EXAMPLE, IF THE FOLLOWING LETTERS WERE WEIGHTED AS SUCH:
    
    A - 1
    E - 2
    G - 4
    M - 7
    P - 5
    S - 3
    T - 6
    
THEN THE WORDS 'TAPES' AND 'GAMES' WOULD SHARE A SCORE (17), EVEN THOUGH NO LETTERS
SHARE A WEIGHT, AND THE MASKING FOR EACH WORD WOULD BE DIFFERENT.
    
IT IS DEFINITELY WORTH REVISITNG THIS TO SEE IF THERE ARE INDEED SUCH CASES IN
PRACTICE, AS IT HAS CONSEQUENCES FOR THE TRIPLET SEARCH.


@author: Ryan Goetz
@email: ryan.m.goetz@gmail.com
"""

import numpy as np
import os

# -----------------------------------------------------------------------------
# CUSTOM FUNCTIONS
# -----------------------------------------------------------------------------

# a vectorized score calculator
def score_calc(word_):
    A = np.ones(26,dtype=np.int64)
    for letter in word_:
        A[ord(letter)-97] *= 0
    A = -1*(A-1)
    score = sum(A*WEIGHTS)
    return score
score_calc = np.vectorize(score_calc)


# Vectorize ord()
def vect_ord(character):
    return ord(character)-97
vect_ord = np.vectorize(vect_ord)

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



# Calculate and save weights to .txt
WEIGHTS = np.zeros(26,dtype=np.int64)
f = open(WORDLE_PATH(),'r')
g = f.read()
for ind in range(len(g)):
    if ind%6 == 5:
        pass
    else:
        WEIGHTS[ord(g[ind])-97] += 1
f.close()
np.savetxt(WEIGHTS_PATH(), WEIGHTS, fmt='%s')

# Sort the wordle words by score (non-unique removed) and write to .txt
f = open(WORDLE_PATH(),'r')
WORDS = np.asarray(f.read().splitlines())
f.close()
SCORES = score_calc(WORDS)
SORTED_WORDS = WORDS[SCORES.argsort()]
SCORES = score_calc(SORTED_WORDS)
_ , UNIQUES = np.unique(SCORES, return_index=True)
SORTED_WORDS = SORTED_WORDS[UNIQUES][::-1]
np.savetxt(WORDS_PATH(), SORTED_WORDS, fmt='%s')


# Calculate the mask for each letter and write its transpose to .txt
WORD_MASK = np.ones((26,len(SORTED_WORDS)), dtype=np.int8)
for idx in range(len(SORTED_WORDS)):
    word = SORTED_WORDS[idx]
    IDXS = vect_ord(list(word))
    WORD_MASK[IDXS,idx] = 0
np.savetxt(MASK_PATH(), WORD_MASK.T,fmt='%s')


