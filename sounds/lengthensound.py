from pydub import AudioSegment
from pydub.playback import play

import os.path
import sys

if len(sys.argv) < 2:
    print("No arguments specified!")
    exit()

for input_wav_file in sys.argv[1:]:

    output_wav_file = "long" + input_wav_file
    target_wav_time = 1200

    if os.path.exists(input_wav_file):
        original_segment = AudioSegment.from_wav(input_wav_file)
        silence_duration = target_wav_time - len(original_segment)
        silenced_segment = AudioSegment.silent(duration=silence_duration)
        combined_segment = original_segment + silenced_segment

        combined_segment.export(output_wav_file, format="wav")
    else:
        print("Error: " + input_wav_file + " not a valid file!")
