import random
import json

class Obfuscator :
    """
    Obfuscator class to obfuscate and deobfuscate text using a character mapping and permutations. """
    def __init__(self, most_common_characters, iter_count=3, window_size=3):

        self.characters_map = {c[0]:i for i, c in enumerate(most_common_characters)}
        self.characters_list =  tuple([c[0] for c in most_common_characters])

        tmp_permutations = list(range(len(self.characters_list)))
        for i in range(iter_count):
            for j in range(len(self.characters_list)):
                # create a random int between 0 and spread
                s = random.randint(0, window_size)
                if(j+s < len(self.characters_list)) :
                    old = tmp_permutations[j]
                    tmp_permutations[j] = tmp_permutations[j+s]
                    tmp_permutations[j+s] = old
        self.permutations = tuple(tmp_permutations)
        tmp_permutations_inverse = [0] * len(self.permutations)
        for i in range(len(self.permutations)):
            tmp_permutations_inverse[self.permutations[i]] = i
        self.permutations_inverse = tuple(tmp_permutations_inverse)

    def obfuscate(self, text):
        """Obfuscate the input text using the character mapping and permutations."""
        return ''.join([
            self.characters_list[self.permutations[self.characters_map[c]]] if c in self.characters_map else c
            for c in text
        ])

    def deobfuscate(self, obfuscated_text):
        """Deobfuscate the input text using the inverse character mapping and permutations."""
        return ''.join([ 
            self.characters_list[self.permutations_inverse[self.characters_map[c]]] if c in self.characters_map else c
            for c in obfuscated_text
        ])

    def to_json(self):
        """Convert the Obfuscator object to a JSON string."""
        return json.dumps({
            'characters_map': self.characters_map,
            'characters_list': self.characters_list,
            'permutations': self.permutations,
            'permutations_inverse': self.permutations_inverse
        })
    
    def from_json(self, json_str) :
        """Load the Obfuscator object from a JSON string."""
        data = json.loads(json_str)
        self.characters_map = data['characters_map']
        self.characters_list = tuple(data['characters_list'])
        self.permutations = tuple(data['permutations'])
        self.permutations_inverse = tuple(data['permutations_inverse'])

