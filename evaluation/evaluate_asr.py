#!/usr/bin/python3

import sys 
import numpy as np 
import os 
import pdb
import re

word_obj = re.compile(r'[a-zA-z]+')

def ct_errs(hyp_seq: list, ref_seq: list):
	D = np.zeros((len(ref_seq) + 1, len(hyp_seq) + 1))
	D[0, :] =  np.arange(len(hyp_seq) + 1)
	D[:, 0] = np.arange(len(ref_seq) + 1)
	for i in range(1, len(ref_seq) + 1):
		for j in range(1, len(hyp_seq) + 1):
			if ref_seq[i - 1] == hyp_seq[j - 1]:
				D[i, j] = D[i - 1, j - 1]
			else:
				sub = D[i - 1, j - 1] + 1
				ins = D[i, j - 1] + 1
				dele = D[i - 1, j] + 1
				D[i, j] = min(sub, ins, dele)
	return D[len(ref_seq), len(hyp_seq)]


def ct_errs_recurs(hyp_seq: list, ref_seq: list):
	#if True:#len(ref_seq) < 30 and len(hyp_seq) < 30:
	#	print("hyp:", hyp_seq)
	#	print("ref:", ref_seq)
	# Resolve len diff'ce
	#diff_in_len = len(hyp_seq) - len(ref_seq)
	#if diff_in_len > 0: # hyp_seq longer
	#	ref_seq = ref_seq + ['<UNK>'] * diff_in_len
	#elif diff_in_len < 0: # ref_seq longer
	#	hyp_seq = hyp_seq + ['<UNK>'] * diff_in_len
	#try:
	#	assert len(hyp_seq) == len(ref_seq)
	#except:
	#	pdb.set_trace()
	# Solve recursively
	if hyp_seq == ref_seq: # all the same
		return 0
	elif sum([int(hyp in ref_seq) for hyp in hyp_seq]) == 0: # none the same
		return len(hyp_seq)
	elif ref_seq[:len(hyp_seq)] == ['<UNK>'] * len(hyp_seq) or \
			hyp_seq[:len(ref_seq)] == ['<UNK>'] * len(ref_seq):
		return float('inf') # going in wrong direction
	elif hyp_seq[0] == ref_seq[0]:
		num_matched = 1
		while hyp_seq[num_matched - 1] == ref_seq[num_matched - 1]:
			if num_matched == len(hyp_seq) or num_matched == len(ref_seq):
				return abs(len(hyp_seq) - len(ref_seq))
			num_matched += 1
		return ct_errs_recurs(hyp_seq[num_matched:], ref_seq[num_matched:])
	else:
		return 1 + min(ct_errs(hyp_seq, ['<UNK>'] + ref_seq),
						ct_errs(['<UNK>'] + hyp_seq, ref_seq))


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
	hyp_seq, ref_seq = list(hyp_sentence), list(ref_sentence)
	return round(100 * ct_errs(hyp_seq, ref_seq) / len(ref_seq), 2)



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
	hyp_seq, ref_seq = hyp_sentence.split(), ref_sentence.split()#word_obj.findall(hyp_sentence), word_obj.findall(ref_sentence)#hyp_sentence.split(), ref_sentence.split()
	return round(100 * ct_errs(hyp_seq, ref_seq) / len(ref_seq), 2)


if __name__ == "__main__":  
	hyp_file = os.path.join("test_cases","hyp_example.txt")
	ref_file = os.path.join("test_cases","ref_example.txt")
	with open(hyp_file,"r",encoding='utf8') as h, open(ref_file,"r",encoding='utf8') as r:
		hyp_sentence = h.read()
		ref_sentence = r.read()
	wer_score = compute_wer(hyp_sentence,ref_sentence)
	cer_score = compute_cer(hyp_sentence,ref_sentence)
	print(wer_score,cer_score)



