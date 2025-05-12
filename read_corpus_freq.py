import os
import random
from collections import Counter
max_lines = -1
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

my_characters_map = {c[0]:i for i, c in enumerate(char_counter.most_common())}
my_characters_list = [c[0] for c in char_counter.most_common()]
print(my_characters_map )
print(my_characters_list)
my_permutations = list(range(len(my_characters_list)))
n_perm = 1 
spread = 2
for i in range(n_perm):
    for j in range(len(my_characters_list)):
        # create a random int between 0 and spread
        s = random.randint(0, spread)
        if(j+s < len(my_characters_list)) :
            old = my_permutations[j]
            my_permutations[j] = my_permutations[j+s]
            my_permutations[j+s] = old
print(my_permutations)
my_permutations_inverse = [0] * len(my_permutations)
for i in range(len(my_permutations)):
    my_permutations_inverse[my_permutations[i]] = i
print(my_permutations_inverse)    
print(f"Total unique characters: {len(my_characters_list)}")

def encrypt(characters_map, characters_list, permutations, text):
    #print (f"char: {char} -> {characters[char]} -> {permutations[characters[char]]} -> {characters[permutations[characters[char]]]} -> {characters[permutations[characters[char]]]} -> {text}")
    return ''.join([ characters_list[permutations[characters_map[c]]] for c in text])

def decrypt(characters_map, characters_list, permutations_inverse, text):
    return ''.join([ characters_list[permutations_inverse[characters_map[c]]] for c in text])

encrypted = encrypt(my_characters_map, my_characters_list, my_permutations, "hello world")
print("encrypt " + encrypted)

print("decrypt " + decrypt(my_characters_map, my_characters_list, my_permutations_inverse, encrypted))
perf_test = True
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
            encrypted_line = encrypt(my_characters_map, my_characters_list, my_permutations, line)
            decrypted_line = decrypt(my_characters_map, my_characters_list, my_permutations_inverse, encrypted_line)
            if line != decrypted_line:
                print(f"Error: {line} != {decrypted_line}")
                raise ValueError("Decryption failed")
            if (lineId < 1000000 and lineId % 100000 == 0 ) or (lineId % 1000000 == 0 ) :
                print(f"Encrypted {lineId} lines, unique characters: {len(char_counter)}")
            if max_lines>0 and lineId >= max_lines:
                break
    end_time = time.time()
    print(f"Encryption took {end_time - start_time} seconds")
