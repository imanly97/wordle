#!/usr/bin/env python
# coding: utf-8

import nltk
from nltk.corpus import words
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def find_potential_words(yellow, used, word, words):
    count = 0
    for letter in word:
        if letter == 0:
            count += 1
            
    if count == 5:
        
        second_temp = []
        for w in words:
            if all(x in list(w) for x in yellow):
                second_temp.append(w)
        
        third_temp = []

        for ws in second_temp:
            if not any(x in list(ws) for x in used):
                third_temp.append(ws)
        
        return third_temp
    
    else:
        first_temp = []
        
        for tword in words:
            green_count = 0

            for i in range(len(tword)):

                if word[i] == tword[i]:

                    green_count += 1

            if green_count == (5-count):
                first_temp.append(tword)
        
        #Trim unuseful words
        second_temp = []

        for w in first_temp:
            if all(x in list(w) for x in yellow):
                second_temp.append(w)

        third_temp = []

        for ws in second_temp:
            if any(x in list(ws) for x in used):
                pass
            else:
                third_temp.append(ws)

        #fourth_temp
        res = []
        [res.append(x) for x in third_temp if x not in res]
        return res

def find_probs(let_counts, potential_words):
    word_counts = []

    for word in potential_words:
        t_val = 0

        for letter in word:
            t_val += let_counts.loc[letter].values
        word_counts.append([word,t_val])

    
    guesses = pd.DataFrame(word_counts)
    guesses['Letter Frequency'] = guesses[1].apply(lambda x : int(x)/43445)
    guesses = guesses.sort_values(by = 'Letter Frequency', ascending = False)
    guesses = guesses.drop(columns = {1})
    guesses = guesses.rename(columns = {0:'Word'})
    print(guesses.head(20))
    
    return guesses


def pruneYellow(used_words, used_hints, potential_words, yellow_pos):
    
    res = []
    yellow_pos['0'].append('z')
    yellow_pos['0'].append('t')
    
    for w in potential_words:
        t = 0
       
        for letter in w:
            
            if letter in yellow_pos.values():
                if letter not in yellow_pos[str(t)]:
                    res.append(w)
                    break
                else:
                    pass
            else:
                res.append(w)
                
            t += 1
    result = []
    [result.append(x) for x in res if x not in result]
    return result

if __name__ == "__main__":

    words = pd.read_csv('words.csv')
    words = words.drop(columns = {'Unnamed: 0'})
    words = words['0']

    letter_distributions = {}
    letter_distributions['a'] = 0
    letter_distributions['b'] = 0
    letter_distributions['c'] = 0
    letter_distributions['d'] = 0
    letter_distributions['e'] = 0
    letter_distributions['f'] = 0
    letter_distributions['g'] = 0
    letter_distributions['h'] = 0
    letter_distributions['i'] = 0
    letter_distributions['j'] = 0
    letter_distributions['k'] = 0
    letter_distributions['l'] = 0
    letter_distributions['m'] = 0
    letter_distributions['n'] = 0
    letter_distributions['o'] = 0
    letter_distributions['p'] = 0
    letter_distributions['q'] = 0
    letter_distributions['r'] = 0
    letter_distributions['s'] = 0
    letter_distributions['t'] = 0
    letter_distributions['u'] = 0
    letter_distributions['v'] = 0
    letter_distributions['w'] = 0
    letter_distributions['x'] = 0
    letter_distributions['y'] = 0
    letter_distributions['z'] = 0

    for word in words:
        for let in word:
            letter_distributions[let] = letter_distributions[let] + 1

    let_counts = pd.DataFrame.from_records(letter_distributions, index = [0]).T

    running = True
    word = [0,0,0,0,0]
    used = []
    yellow = []
    used_words = []
    used_hints = []
    yellow_pos = {}
    yellow_pos['0'] = []
    yellow_pos['1'] = []
    yellow_pos['2'] = []
    yellow_pos['3'] = []
    yellow_pos['4'] = []
    
    while running == True:
        guess = str(input("Enter your guess in lowercase! "))
        hints = str(input("Enter your hint results in the form: ynygn (Yellow, None, Green) "))
        pos = 0
        used_words.append(guess)
        used_hints.append(hints)

        for let in hints:
            if let == 'g':
                word[pos] = guess[pos]
            if let == 'y':
                yellow.append(guess[pos])
            if let == 'n' and guess[pos] not in yellow:
                used.append(guess[pos])
            pos += 1
        
        potential_words = find_potential_words(yellow, used, word, words)
        print('Potential words:', len(potential_words))
        potential_words = pruneYellow(used_words, used_hints, potential_words, yellow_pos)
        guesses = find_probs(let_counts, potential_words)

        if len(guesses) == 1:
            running = False


        count = 0
        for letter in word:
            if letter != 0:
                count += 1
            if count == 5:
                running = False
