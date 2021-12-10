import argparse
import os
import pdb

TSV_NAMES = ["validated", "invalidated", "other", "train", "test", "dev"]
# MV_AUDIO = True

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--transl-tsv", type=str, required=True, help="path to tsv with english translations")
    parser.add_argument("--lang-dir", type=str, required=True, help="path to directory for all language data")
    parser.add_argument("--move-audio", action='store_true', help="whether to move audio mp3 or wav files from clips directory")

    args = parser.parse_args()

    if args.lang_dir[-1] != '/':
        args.lang_dir = args.lang_dir + '/'

    print("Creating package directory", flush=True)

    if not os.path.exists(args.lang_dir + 'package'):
        os.system("mkdir {}package".format(args.lang_dir))

    print("Opening tsv file", flush=True)

    with open(args.transl_tsv, 'r') as f:
        tsv_lines = f.readlines()
    tsv_lines = tsv_lines[1:]

    bare_audio_paths = [line.split('\t')[0] for line in tsv_lines]
    bare_audio_paths = [p.split('/')[-1] for p in bare_audio_paths]

    print("Essembling file names", flush=True)

    path2transc = {}
    iterator = 0
    for fn in [args.lang_dir + tsvname + '.tsv' for tsvname in TSV_NAMES]:
        with open(fn, 'r') as f:
            transc_lines = f.readlines()[1:]
        for line in transc_lines:
            items = line.split('\t')
            path, sent = items[1], items[2]
            if path in bare_audio_paths:
                path2transc[path] = sent
            iterator += 1
            if iterator % 1000 == 0:
                print(iterator, end=' ', flush=True)
    print()

    print("Assembling transcriptions and moving audio clips", flush=True)

    transcs = []
    iterator = 0
    for path in bare_audio_paths:
        transcs.append(path2transc[path])
        
        if args.move_audio:
            # move audio file to package
            mv_str = "mv {}clips/{} {}package".format(args.lang_dir, path, args.lang_dir)
            os.system(mv_str)
            iterator += 1
            print(iterator, end=' ', flush=True)
    print()

    print("Saving transcriptions", flush=True)

    transcs = [t + '\n' for t in transcs]
    with open(args.lang_dir + "package/ordered_transcriptions.txt", 'w') as f:
        f.writelines(transcs)

    print("Copying translation tsv into package", flush=True)

    cp_str = "cp {} {}package".format(args.transl_tsv, args.lang_dir)
    os.system(cp_str)

    print("=====================================================================")
    print("done -- SUCCESSFUL")
    print("Verify that {}package/ordered_transcriptions.txt is written and has the same number of lines as {} (off by one)".format(\
            args.lang_dir, args.transl_tsv))
    if args.move_audio:
        print("Verify that {}package/*mp3 is filled and contains the same number of lines as well".format(args.lang_dir))
    print("Now you may execute mv {}package ~/anlp11711_proj/<LANG>_data".format(args.lang_dir))
    print("And you may rm -rf {}clips".format(args.lang_dir))
    print("And once you do that... go into {} and execute < :%s/common_voice_id/\/home\/n8rob\/anlp11711_proj\/<LANG>_data\/package\/common_voice_id/g >".format(\
            args.transl_tsv))
    print("And then move on to running lattice.py inside of your allosaurus version")
