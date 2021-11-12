#!/usr/bin/python3

import sys 
import numpy as np 
import os 
import unidecode

def error_rate_computation(hyp_lst, ref_lst): 
    # initialize table 
    rows = len(hyp_lst)+1
    cols = len(ref_lst) +1
    dp_table = np.zeros((rows, cols))

    # fill in first row and column 
    for row in range(rows): 
        dp_table[row][0] = row 
    for col in range(cols): 
        dp_table[0][col] = col 

    # dp computation 
    for row in range(1, rows): 
        for col in range(1, cols): 
            if hyp_lst[row-1] != ref_lst[col-1]: 
                dp_table[row][col] = 1+ min(dp_table[row-1][col-1], 
                                            dp_table[row-1][col], 
                                            dp_table[row][col-1])
            else: 
                dp_table[row][col] = dp_table[row-1][col-1]

    changes = dp_table[rows-1][cols-1]
    
    er = changes / len(ref_lst)
    return round(er*100,2)

def compute_cer(hyp_sentence="",ref_sentence=""):
    """
    Inputs: 
    hyp_sentence: str- Sentence of text from the ASR Hypothesis
    ref_sentence: str-Sentence of text from the Ground Truth Reference
    Returns:
    cer_score: float- CER Score as a floating point number rounded to two decimal places
    For example, for 
    REF: This great machine can recognize speech
    HYP: This ~~~~~~ machine can wreck~~~~~a~~~~~~nice beach
    return 38.46        
    """
    ## Fill your code here
    return error_rate_computation(hyp_sentence, ref_sentence)


def compute_wer(hyp_sentence="",ref_sentence=""):
    """
    Inputs: 
    hyp_sentence: str- Sentence of text from the ASR Hypothesis
    ref_sentence: str-Sentence of text from the Ground Truth Reference
    Returns:
    wer_score: float- WER Score as a floating point number rounded to two decimal places
    For example, for 
    REF: This great machine can recognize speech
    HYP: This ~~~~~~ machine can wreck~~~~~a~~~~~~nice beach
    return 83.33        
    """
    ## Fill your code here
    hyp_lst = hyp_sentence.split(" ")
    ref_lst = ref_sentence.split(" ")
    return error_rate_computation(hyp_lst, ref_lst)


def file_wer(hyp_file, ref_file):
    """
    Inputs: 
    hyp_file: str- file path of text from the ASR Hypothesis
    ref_file: str- file path of text from the Ground Truth Reference
    Returns:
    wer_score: float- average of WER score of all sentences in files
    """
    with open(hyp_file) as h:
        hyp_lines = h.readlines()
    
    with open(ref_file) as r:
        ref_lines = r.readlines()

    count = len(hyp_lines)
    total_wer = 0

    for i in range(1,count+1):
        hyp_sent = unidecode.unidecode(hyp_lines[-i]).strip()
        ref_sent = unidecode.unidecode(ref_lines[-i]).strip()
        wer = compute_wer(hyp_sent, ref_sent)
        total_wer += wer

    return total_wer/count




if __name__ == "__main__":  

    hyp_file = "output_2500.txt"
    ref_file = "fisher_dev.es.nopunc.lower"
    #ref_file = "fisher_train_subset.es.nopunc.lower"

    print(hyp_file, ref_file, file_wer(hyp_file, ref_file))







    