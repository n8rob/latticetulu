from evaluate_asr import compute_cer
import numpy as np 
import argparse

def calc_per(hyp, ref):
    if type(ref) == str:
        with open(ref, 'r') as f:
            refs = f.readlines()
    elif type(ref) == list:
        refs = ref
    else:
        raise TypeError("reference should be str or list")
    refs = [ref.strip().replace(' ', '').replace('<blk>', '') for ref in refs]

    if type(hyp) == str:
        with open(hyp, 'r') as f:
            hyps = f.readlines()
    elif type(hyp) == list:
        hyps = hyp
    else:
        raise TypeError("hypothesis should be str or list")
    hyps = [hyp.strip().replace(' ', '').replace('<blk>', '') for hyp in hyps]

    cers = []
    for r, h in zip(refs, hyps):
        cer = compute_cer(hyp_sentence=h,ref_sentence=r)
        cers.append(cer)
        print('ref:', r, "hyp:", h, 'cer:', cer)

    per = np.mean(cers)
    print("PER:", per)

    return per, cers

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--hyp-file", type=str, required=True) #, help="directory for input wav files, or may be csv with wav file paths")
    parser.add_argument("--ref-file", type=str, required=True) #, help="path for output lattice file")

    args = parser.parse_args()

    per = calc_per(hyp=args.hyp_file, ref=args.ref_file)
