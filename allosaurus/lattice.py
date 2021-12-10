import argparse
import os
from os import path
from pydub import AudioSegment
import csv
from allosaurus.app import read_recognizer
model = read_recognizer()

import re
import pdb

NONALPH_OBJ = re.compile(r'[^a-zA-Z ]')

"""
Example output from model.recognize:

    [[('æ', 0.56984365), ('ɛ', 0.15730369), ('ɒ', 0.094979)], [('l', 0.78301376), ('l̪', 0.1792332), ('lː', 0.013551216)], [('u', 0.20662732), ('ɨ', 0.19654621), ('uː', 0.110776655)], [('s', 0.33875775), ('<blk>', 0.29121703), ('z', 0.102964915)], [('ɔ', 0.45242321), ('ɑ', 0.25989923), ('<blk>', 0.10862362)], [('ɹ', 0.86626154), ('ɾ', 0.068385616), ('<blk>', 0.025983471)], [('s', 0.74260235), ('z', 0.19224834), ('s̪', 0.037900772)]]
"""

def wav2lattice(infile, lang_id='ipa'):
    """
    """
    if infile[-3:] == 'mp3':
        # Convert mp3 to wav
        src = infile # Leckily, strings are not mutable
        dst = "temp.wav"
        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")
        infile = dst
    elif infile[-3:] != 'wav':
        raise NotImplementedError("Must be .mp3 or .wav files")

    list_list_tups = model.recognize(infile, lang_id=lang_id, topk=3)

    text = ""
    for i, frame in enumerate(list_list_tups):
        for phone, score in frame:
            line = [str(i), str(i+1), phone, phone, str(score)]
            line_text = '\t'.join(line) + '\n'
            text += line_text

    return text

def wavs2lattices(infiles, outfile="lattice.lat", lang_id='ipa'):

    if type(infiles) == str:
        if infiles[-1] != '/':
            infiles = infiles + '/'
        infiles = [infiles + fn for fn in os.listdir(infiles)]
    lats = []
    bad_idxs = []
    print("Total files:", len(infiles))
    for fidx, inf in enumerate(infiles): # n8hack
        print(fidx, end=' ', flush=True)
        try:
            lat_here = wav2lattice(inf, lang_id=lang_id)
        except:
            print("SKIPPED", end=' ')
            bad_idxs.append(fidx)
            # raise
            continue
        if lat_here == '':
            print("SKIPPED", end=' ')
            bad_idxs.append(fidx)
            continue
        lats.append(lat_here)
    print()
    text = '\n'.join(lats)

    with open(outfile, 'w') as f:
        f.write(text.strip() + '\n\n')
    
    print("Lattice written to", outfile, flush=True)
    print(len(bad_idxs), "SKIPPED files", flush=True)
    print('done')
    return bad_idxs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wav-path", type=str, required=True, help="directory for input wav files, or may be csv with wav file paths")
    parser.add_argument("--out-file", type=str, default='lattice.lat', help="path for output lattice file")
    parser.add_argument("--lang-id", type=str, default='tcy', help='Language code for recognition, (e.g. "tcy" for Tulu,'\
                        '"swh" for Kiswahili, "tam" for Tamil, "eng" for English, "ipa" for IPA);'\
                        'See ./allosaurus/pretrained/uni2005/inventory/index.json')

    args = parser.parse_args()

    extnn = args.wav_path[-3:]
    if extnn in ['csv', 'tsv']:
        delim = ',' if extnn == 'csv' else '\t'
        fns, transls = [], []
        with open(args.wav_path, 'r') as csvf:
            text = csvf.read()
            lines = text.split('\n')[1:-1]
            for line in lines:
                row = line.split(delim)
                # tulu_spliced_audio/kudla_cafe/kudla_cafe_1.mp3 -> ../tulu_data/Kudla_Cafe_1/cleaned_kudla_cafe_1.mp3
                fns.append(row[0].replace('tulu_spliced_audio/kudla_cafe/', '../tulu_data/Kudla_Cafe_1/cleaned_'))
                try:
                    real_transl = re.sub(NONALPH_OBJ, '', row[1])
                except:
                    pdb.set_trace()
                transls.append(real_transl)
        bad_idxs = wavs2lattices(fns, outfile=args.out_file, lang_id=args.lang_id)
        # Get rid of unpaired translations
        for bad_idx in bad_idxs[::-1]:
            transls.pop(bad_idx)
        print(len(transls), 'translations', flush=True)
        with open(args.out_file.replace('.lat', '_eng.txt'), 'w') as f:
            f.write('\n'.join(transls)+'\n')
    else:
        wavs2lattices(args.wav_path, outfile=args.out_file, lang_id=args.lang_id)

