import os
import random
import obfuscator
from collections import Counter
max_lines = 100000
with open('C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf.txt', 'r', encoding="UTF8") as f:
    lineId = 0
    # Initialize a Counter to count the frequency of each word
    char_counter = Counter()
    for line in f:
        lineId += 1
        # Remove leading and trailing whitespace
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
        for char in line:
            # Increment the count for the character
            char_counter[char] += 1
        if (lineId < 1000000 and lineId % 100000 == 0 ) or (lineId % 1000000 == 0 ) :
            print(f"Processed {lineId} lines, unique characters: {len(char_counter)}")
        if max_lines>0 and lineId >= max_lines:
            break

o = obfuscator.Obfuscator(char_counter.most_common(), iter_count=3, window_size=3)

encrypted = o.obfuscate("hello world")
print("encrypt " + encrypted)
print("decrypt " + o.deobfuscate(encrypted))
json_str = o.to_json()

o2 = obfuscator.Obfuscator([])
o2.from_json(json_str)
print("obfuscator2.obfuscate() ", o2.obfuscate("hello world"))

#print("obfuscator.to_json() ", obfuscator.to_json())
#print("obfuscator.from_json() ", obfuscator.from_json(obfuscator.to_json()))

perf_test = True
max_lines_2 = 1000000
if perf_test:
    # Test the performance of the encryption function
    import time
    start_time = time.time()
    with open('C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf.txt', 'r', encoding="UTF8") as f:
        lineId = 0
        # Initialize a Counter to count the frequency of each word
        for line in f:
            lineId += 1
            # Remove leading and trailing whitespace
            line = line.strip()
            encrypted_line = o2.obfuscate(line)
            decrypted_line = o2.deobfuscate(encrypted_line)
            if line != decrypted_line:
                print(f"Error: {line} != {decrypted_line}")
                raise ValueError("Decryption failed")
            if (lineId < 1000000 and lineId % 8100000 == 0 ) or (lineId % 1000000 == 0 ) :
                print(f"Encrypted {lineId} lines, unique characters: {len(char_counter)}")
            if max_lines_2>0 and lineId >= max_lines_2:
                break
    end_time = time.time()
    print(f"Encryption took {end_time - start_time} seconds")
