# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 23:04:04 2022

This script is intended to identify the optimal three starting words for Quordle,
a game similar to Wordle, found here: https://www.quordle.com/

This simple approach only values letter identification, not letter position.
That is, the score/weight of a particular word is independent of the order of 
the letters within the word. Furthermore, word scores do not benefit from
repeated letters. If they were appropriate English words, 'aaabb', 'ababa', and
'abbbb' would all receive the same score.

With the simple approach we are trying to find a triplet of words that has
maximal sum of their scores, while satisfying the condition that no words of
the triplet contain letters from any of the other words.

@author: Ryan Goetz
@email: ryan.m.goetz@gmail.com
"""

import numpy as np
import os
from make_data import DATA_PATH, WORDLE_PATH, WEIGHTS_PATH, WORDS_PATH, MASK_PATH

# -----------------------------------------------------------------------------
# CUSTOM FUNCTIONS
# -----------------------------------------------------------------------------

# A vectorized score calculator
def score_calc(word_):
    A = np.ones(26,dtype=np.int64)
    for letter in word_:
        A[ord(letter)-97] *= 0
    A = -1*(A-1)
    score = sum(A*WEIGHTS)
    return score
score_calc = np.vectorize(score_calc)


# Vectorize ord() and set 'a' to 0
def vect_ord(character):
    return ord(character)-97
vect_ord = np.vectorize(vect_ord)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


# this seems like a daunting series of loops, but the break conditions actually
# mean the total number of calculations is very small
WEIGHTS = np.loadtxt(WEIGHTS_PATH(), dtype=np.int64)
SORTED_WORDS = np.loadtxt(WORDS_PATH(), dtype=str)
WORD_MASK = np.loadtxt(MASK_PATH())
WORD_MASK = WORD_MASK.T
SCORES = score_calc(SORTED_WORDS)
MAX_SCORE = SCORES[0]
BATCH_1 = SORTED_WORDS[SCORES >= MAX_SCORE//3]
SCORES_1 = SCORES[:len(BATCH_1)] 
for word_1, score_1 in zip(BATCH_1, SCORES_1):
    if score_1 < MAX_SCORE//3:
        break
    letter_ords_1 = vect_ord(list(word_1)) 
    first_mask = np.prod(WORD_MASK[letter_ords_1], axis=0)
    first_mask = first_mask != 0
    BATCH_2 = SORTED_WORDS[first_mask]
    SCORES_2 = SCORES[first_mask]
    BATCH_2 = BATCH_2[SCORES_2 >= (MAX_SCORE-score_1)//2]
    SCORES_2 = SCORES_2[:len(BATCH_2)]
    for word_2, score_2 in zip(BATCH_2, SCORES_2):
        if score_2 < (MAX_SCORE-score_1)//2:
            break
        letter_ords_2 = vect_ord(list(word_2))
        second_mask = np.prod(WORD_MASK[letter_ords_2], axis=0)
        second_mask = second_mask != 0
        second_mask = first_mask*second_mask
        BATCH_3 = SORTED_WORDS[second_mask]
        SCORES_3 = SCORES[second_mask]
        BATCH_3 = BATCH_3[SCORES_3 >= (MAX_SCORE-score_1-score_2)]
        SCORES_3 = SCORES[:len(BATCH_3)]
        for word_3, score_3 in zip(BATCH_3, SCORES_3):
            if score_3 < (MAX_SCORE-score_1-score_2):
                break
            if score_1 + score_2 + score_3 > MAX_SCORE:
                MAX_SCORE = score_1+score_2+score_3
                TRIPLET = [word_1, word_2, word_3]           
print(TRIPLET)
    

