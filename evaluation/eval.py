import argparse
from per import *
from allo_recognize import * # For now
import re
import epitran
from scipy import stats
import pdb

"""'hat-Latn-bab')
        epi = epitran.Epitran('fra-Latn')
        epi = epitran.Epitran('spa-Latn')
"""

NONALPH_OBJ = re.compile(r'[\.\?\!\/\\\,\[\]\(\)\{\}\;\:\"\'\%\*]')
SPACE_OBJ = re.compile(r'\s+')
EPI_LANGS = {"fra":"fra-Latn", "spa":"spa-Latn", "hat":"hat-Latn-bab",
        "ara":"ara-Arab", "cat":"cat-Latn", "eng":"eng-Latn",
        "ind":"ind-Latn", "tam":"tam-Taml", "fas":"fas-Arab"
        }
ALLO_LANGS = {"fra":"fra", "spa":"spa",
        "ara":"arb", "cat":"cat", "eng":"eng",
        "ind":"ind", "tam":"tam", "fas":"pes"
        }

def clean_sent(sent):
    # sent = sent.lower()
    sent = sent.strip()
    sent = re.sub(SPACE_OBJ, ' ', sent)
    sent = re.sub(NONALPH_OBJ, '', sent)
    return sent

def get_refs(transc_file, test_len, epi_lang):
    with open(transc_file, 'r') as f:
        transcs = f.readlines()
    transcs = transcs[-test_len:]

    epi = epitran.Epitran(epi_lang)

    # clean
    transcs = [clean_sent(t) for t in transcs]
    # get phoneme transcriptions
    phones = [epi.transliterate(t).replace(' ', '') for t in transcs]
    return phones

def sampled_sig_test(ar_base, ar_cand):
    stat, p = stats.wilcoxon(ar_base, ar_cand)
    return p

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--test-len", type=int, default=187, help="number of test sentences")
    parser.add_argument("--out-hyp", type=str, required=True, help="output file from lattice tm")
    parser.add_argument("--transcriptions", type=str, required=True, help="transcriptions file")
    parser.add_argument("--lang", type=str, required=True, help="language (e.g. one of the following): "\
                                                                "['spa', 'hat', 'fra', 'ara', 'cat', "\
                                                                "'eng', 'ind', 'tam', 'fas']")
    parser.add_argument("--audio-csv", type=str, required=True, help="*csv or *tsv file with audio file paths")

    args = parser.parse_args()

    with open(args.out_hyp, 'r') as f:
        hyp_lines = f.readlines()
    hyp_lines = hyp_lines[-args.test_len:]

    ref_lines = get_refs(args.transcriptions, args.test_len, EPI_LANGS[args.lang])

    print()
    print("### RESULTS FROM LATTICE TM ###")
    print()
    per_score, hyp_pers = calc_per(hyp=hyp_lines, ref=ref_lines) 
   
    delim = ',' if args.audio_csv[-3:] == 'csv' else '\t'
    with open(args.audio_csv) as f:
        lines = f.readlines()
    aud_lines = lines[-int(args.test_len):]
    audio_fns = [line.split(delim)[0] for line in aud_lines]

    allo_transcs = transliterations(audio_fns,ALLO_LANGS[args.lang])

    print()
    print("### RESULTS FROM ALLOSAURUS ALONE ###")
    print()
    allo_score, basel_pers = calc_per(hyp=allo_transcs, ref=ref_lines)

    print("LatticeTM PER:", per_score)
    print("Allosaurus PER:", allo_score)

    p_val = sampled_sig_test(basel_pers, hyp_pers)
    print("\tstatistical significance p =", p_val)
