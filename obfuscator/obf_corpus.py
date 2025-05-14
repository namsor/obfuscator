import os
import random
from collections import Counter
import obfuscator
import time
max_lines = -1
# read the obfuscator key from a file
with open('C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf_key.json', 'r', encoding="UTF8") as f:
    json_str = f.read()

o2 = obfuscator.Obfuscator([])
o2.from_json(json_str)

with open('C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf.txt', 'r', encoding="UTF8") as f, \
        open('C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf_obf.json', 'w', encoding="UTF8") as f_out:
    start_time = time.time()
    lineId = 0
    # Initialize a Counter to count the frequency of each word
    for line in f:
        lineId += 1
        # Remove leading and trailing whitespace
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
        obf_line = o2.obfuscate(line)
        f_out.write(obf_line + "\n")
        if (lineId < 1000000 and lineId % 100000 == 0 ) or (lineId % 1000000 == 0 ) :
            print(f"Processed {lineId} lines, line: {line} --> obfuscated line: {obf_line}")
        if max_lines>0 and lineId >= max_lines:
            break
    end_time = time.time()
    print(f"Encryption took {end_time - start_time} seconds")
