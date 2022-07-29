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

import numpy as np
import os

# -----------------------------------------------------------------------------
# CUSTOM FUNCTIONS
# -----------------------------------------------------------------------------

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
TRANS = translate(WORDS)
_ , UNIQUES = np.unique(TRANS, return_index = True)
WORDS = WORDS[UNIQUES]
SCORES = score_calc(WORDS)
SORTED_WORDS = WORDS[SCORES.argsort()][::-1]
#SCORES = score_calc(SORTED_WORDS)
#_ , UNIQUES = np.unique(SCORES, return_index=True)
#SORTED_WORDS = SORTED_WORDS[UNIQUES][::-1]
np.savetxt(WORDS_PATH(), SORTED_WORDS, fmt='%s')


# Calculate the mask for each letter and write its transpose to .txt
WORD_MASK = np.ones((26,len(SORTED_WORDS)), dtype=np.int8)
for idx in range(len(SORTED_WORDS)):
    word = SORTED_WORDS[idx]
    IDXS = v_ord(list(word))
    WORD_MASK[IDXS,idx] = 0
np.savetxt(MASK_PATH(), WORD_MASK.T,fmt='%s')


