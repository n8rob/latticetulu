from allosaurus.app import read_recognizer
from pydub import AudioSegment
model = read_recognizer()

def transliterations(filenames,allo_lang):
    rec_strs= []
    for fn_i, fn in enumerate(filenames):
        print(fn_i, end=' ', flush=True)
        if fn[-3:] == 'mp3':
            # Convert mp3 to wav
            src = fn # Leckily, strings are not mutable
            dst = "temp.wav"
            sound = AudioSegment.from_mp3(src)
            sound.export(dst, format="wav")
            fn = dst
        elif fn[-3:] != 'wav':
            raise NotImplementedError("Must be .mp3 or .wav files")
        rec_str = model.recognize(fn, lang_id=allo_lang)
        rec_strs.append(rec_str)
    print()
    return rec_strs

if __name__ == "__main__":
    with open("allosaurus_transcripts.txt", 'w') as f:
        f.write('')

    template = "sound_final{}.wav"
    for i in range(1, 16):
        fn = template.format(i)
        rec_str = model.recognize(fn, lang_id='arb')
        print(rec_str)
        with open("allosaurus_transcripts.txt", 'a') as f:
            f.write(rec_str + '\n')
