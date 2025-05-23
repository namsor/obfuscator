import obfuscator
import argparse
from collections import Counter

def read_corpus_freq(input_file_path, max_lines=-1):
    """
    Read the corpus and count the frequency of each character.
    """
    # Initialize a Counter to count the frequency of each word
    char_counter = Counter()
    with open(input_file_path, 'r', encoding="UTF8") as f:
        lineId = 0
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
    return char_counter

def generate_obfuscator_key(char_counter, key_name, key_file_path, flair_file_path):
    """
    Generate the obfuscator key and write it to a file.
    """
    o = obfuscator.Obfuscator(char_counter.most_common(), key_name=key_name)
    o_key =  o.to_json()
    # write the key to a file
    print(f"save key_name: {key_name} to file {key_file_path}")
    with open(key_file_path, 'w', encoding="UTF8") as f:
        f.write(o_key)
    # create a FLAIR dictionary file
    dictionary = obfuscator.Dictionary(True)
    for c in o.characters_list :
        dictionary.add_item(c)
    dictionary.save(flair_file_path)
    return o_key

def obfuscate_corpus(input_file_path, output_file_path, obfuscator_key, max_lines=-1):
    """
    Obfuscate the corpus using the obfuscator key.
    """
    o2 = obfuscator.Obfuscator([])
    o2.from_json(obfuscator_key)
    
    with open(input_file_path, 'r', encoding="UTF8") as f, \
            open(output_file_path, 'w', encoding="UTF8") as f_out:
        lineId = 0
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

def deobfuscate_corpus(input_file_path, output_file_path, obfuscator_key, max_lines=-1):
    """
    Deobfuscate the corpus using the obfuscator key.
    """
    o2 = obfuscator.Obfuscator([])
    o2.from_json(obfuscator_key)
    
    with open(input_file_path, 'r', encoding="UTF8") as f, \
            open(output_file_path, 'w', encoding="UTF8") as f_out:
        lineId = 0
        for line in f:
            lineId += 1
            # Remove leading and trailing whitespace
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            deobf_line = o2.deobfuscate(line)
            f_out.write(deobf_line + "\n")
            if (lineId < 1000000 and lineId % 100000 == 0 ) or (lineId % 1000000 == 0 ) :
                print(f"Processed {lineId} lines, line: {line} --> deobfuscated line: {deobf_line}")
            if max_lines>0 and lineId >= max_lines:
                break

def main():
    parser = argparse.ArgumentParser(description="Corpus Obfuscator CLI")
    # add arguments for the CLI
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("--output_file", help="Path to the output file")
    parser.add_argument("--key_name", help="Name of the obfuscator key")
    parser.add_argument("--max_lines", type=int, default=-1, help="Maximum number of lines to process")
    parser.add_argument("--obfuscate", action="store_true", help="Obfuscate the corpus")
    parser.add_argument("--deobfuscate", action="store_true", help="Deobfuscate the corpus")
    parser.add_argument("--gen_key", action="store_true", help="Generate obfuscator key and FLAIR dict file")
    parser.add_argument("--key_file", help="Path to the obfuscator key file")
    parser.add_argument("--flair_file", help="Path to the FLAIR dictionary file")

    args = parser.parse_args()
    # check if the user wants to generate a key
    if args.gen_key:
        if not args.key_name or not args.key_file:
            print("Please provide a key name and key file path to generate the obfuscator key.")
            return
        if not args.flair_file:
            print("Please provide a flair file path to obfuscate the corpus.")
            return
        char_counter = read_corpus_freq(args.input_file, args.max_lines)
        generate_obfuscator_key(char_counter, args.key_name, args.key_file, args.flair_file)
    elif args.obfuscate:
        if not args.key_file:
            print("Please provide a key file path to obfuscate the corpus.")
            return
        if not args.output_file:
            print("Please provide an output file path to obfuscate the corpus.")
            return
        with open(args.key_file, 'r', encoding="UTF8") as f:
            obfuscator_key = f.read()
            # read the obfuscator key from the key_file    
            obfuscate_corpus(args.input_file, args.output_file, obfuscator_key, args.max_lines)
    elif args.deobfuscate:
        if not args.key_file:
            print("Please provide a key file path to deobfuscate the corpus.")
            return
        if not args.output_file:
            print("Please provide an output file path to deobfuscate the corpus.")
            return
        with open("args.key_file", 'r', encoding="UTF8") as f:
            obfuscator_key = f.read()
            # read the obfuscator key from the key_file    
            deobfuscate_corpus(args.input_file, args.output_file, obfuscator_key, args.max_lines)

if __name__ == "__main__":
    main()