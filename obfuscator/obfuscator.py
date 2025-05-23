import random
import json
from os import PathLike
from pathlib import Path
from typing import Union
import logging as log

class Dictionary:
    """This class holds a dictionary that maps strings to unique integer IDs.

    Used throughout Flair for representing words, tags, characters, etc.
    Handles unknown items (<unk>) and flags for multi-label or span tasks.
    Items are stored internally as bytes for efficiency.
    """

    def __init__(self, add_unk: bool = True) -> None:
        """Initializes a Dictionary.

        Args:
            add_unk (bool, optional): If True, adds a special '<unk>' item.
                Defaults to True.
        """
        # init dictionaries
        self.item2idx: dict[bytes, int] = {}
        self.idx2item: list[bytes] = []
        self.add_unk = add_unk
        self.multi_label = False
        self.span_labels = False
        # in order to deal with unknown tokens, add <unk>
        if add_unk:
            self.add_item("<unk>")

    def remove_item(self, item: str):
        """Removes an item from the dictionary.

        Note: This operation might be slow for large dictionaries as it involves
        list removal. It currently doesn't re-index subsequent items.

        Args:
            item (str): The string item to remove.
        """
        bytes_item = item.encode("utf-8")
        if bytes_item in self.item2idx:
            self.idx2item.remove(bytes_item)
            del self.item2idx[bytes_item]

    def add_item(self, item: str) -> int:
        """Adds a string item to the dictionary.

        If the item exists, returns its ID. Otherwise, adds it and returns the new ID.

        Args:
            item (str): The string item to add.

        Returns:
            int: The integer ID of the item.
        """
        bytes_item = item.encode("utf-8")
        if bytes_item not in self.item2idx:
            self.idx2item.append(bytes_item)
            self.item2idx[bytes_item] = len(self.idx2item) - 1
        return self.item2idx[bytes_item]

    def get_idx_for_item(self, item: str) -> int:
        """Retrieves the integer ID for a given string item.

        Args:
            item (str): The string item.

        Returns:
            int: The integer ID. Returns 0 if item is not found and `add_unk` is True.

        Raises:
            IndexError: If the item is not found and `add_unk` is False.
        """
        item_encoded = item.encode("utf-8")
        if item_encoded in self.item2idx:
            return self.item2idx[item_encoded]
        elif self.add_unk:
            return 0
        else:
            log.error(f"The string '{item}' is not in dictionary! Dictionary contains only: {self.get_items()}")
            log.error(
                "You can create a Dictionary that handles unknown items with an <unk>-key by setting add_unk = True in the construction."
            )
            raise IndexError

    def get_idx_for_items(self, items: list[str]) -> list[int]:
        """Retrieves the integer IDs for a list of string items. (No cache version)"""
        if not items:
            return []

        indices: list[int] = []
        unk_idx = 0  # Assuming <unk> is index 0 if add_unk is True

        for item in items:
            item_bytes = item.encode("utf-8")
            idx = self.item2idx.get(item_bytes)  # Look up bytes directly

            if idx is not None:
                indices.append(idx)
            elif self.add_unk:
                indices.append(unk_idx)  # Append 0 for <unk>
            else:
                # Raise error if not found and add_unk is False
                log.error(f"Item '{item}' not found in dictionary (add_unk=False).")
                # ... (error logging) ...
                raise IndexError(f"Item '{item}' not found in dictionary.")

        return indices

    def get_items(self) -> list[str]:
        """Returns a list of all items in the dictionary in order of their IDs."""
        return [item.decode("UTF-8") for item in self.idx2item]

    def __len__(self) -> int:
        """Returns the total number of items in the dictionary."""
        return len(self.idx2item)

    def get_item_for_index(self, idx: int) -> str:
        """Retrieves the string item corresponding to a given integer ID.

        Args:
            idx (int): The integer ID.

        Returns:
            str: The string item.

        Raises:
            IndexError: If the index is out of bounds.
        """
        return self.idx2item[idx].decode("UTF-8")

    def has_item(self, item: str) -> bool:
        """Checks if a given string item exists in the dictionary."""
        return item.encode("utf-8") in self.item2idx

    def set_start_stop_tags(self) -> None:
        """Adds special <START> and <STOP> tags to the dictionary (often used for CRFs)."""
        self.add_item("<START>")
        self.add_item("<STOP>")

    def is_span_prediction_problem(self) -> bool:
        """Checks if the dictionary likely represents BIOES/BIO span labels.

        Returns True if `span_labels` flag is set or any item starts with 'B-', 'I-', 'S-'.

        Returns:
            bool: True if likely span labels, False otherwise.
        """
        if self.span_labels:
            return True
        return any(item.startswith(("B-", "S-", "I-")) for item in self.get_items())

    def start_stop_tags_are_set(self) -> bool:
        """Checks if <START> and <STOP> tags have been added."""
        return {b"<START>", b"<STOP>"}.issubset(self.item2idx.keys())

    def save(self, savefile: PathLike):
        """Saves the dictionary mapping to a file using pickle.

        Args:
            savefile (PathLike): The path to the output file.
        """
        import pickle

        with open(savefile, "wb") as f:
            mappings = {"idx2item": self.idx2item, "item2idx": self.item2idx}
            pickle.dump(mappings, f)

    def __setstate__(self, d: dict) -> None:
        self.__dict__ = d
        # set 'add_unk' if the dictionary was created with a version of Flair older than 0.9
        if "add_unk" not in self.__dict__:
            self.__dict__["add_unk"] = b"<unk>" in self.__dict__["idx2item"]

    @classmethod
    def load_from_file(cls, filename: Union[str, Path]) -> "Dictionary":
        """Loads a Dictionary previously saved using the `.save()` method.

        Args:
            filename (Union[str, Path]): Path to the saved dictionary file.

        Returns:
            Dictionary: The loaded Dictionary object.
        """
        import pickle

        with Path(filename).open("rb") as f:
            mappings = pickle.load(f, encoding="latin1")
            idx2item = mappings["idx2item"]
            item2idx = mappings["item2idx"]

        # set 'add_unk' depending on whether <unk> is a key
        add_unk = b"<unk>" in idx2item

        dictionary: Dictionary = Dictionary(add_unk=add_unk)
        dictionary.item2idx = item2idx
        dictionary.idx2item = idx2item
        return dictionary


    def __eq__(self, o: object) -> bool:
        """Checks if two Dictionary objects are equal based on content and flags."""
        if not isinstance(o, Dictionary):
            return False
        return self.item2idx == o.item2idx and self.idx2item == o.idx2item and self.add_unk == o.add_unk

    def __str__(self) -> str:
        tags = ", ".join(self.get_item_for_index(i) for i in range(min(len(self), 50)))
        return f"Dictionary with {len(self)} tags: {tags}"



class Obfuscator :
    """
    Obfuscator class to obfuscate and deobfuscate text using a character mapping and permutations. 
    Roundtrip processing 195M names with 3k unique characters takes about 30 minutes.
    """
    def __init__(self, most_common_characters, key_name="", iter_count=3, window_size=3):
        self.key_name = key_name
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
            'key_name': self.key_name,
            'characters_map': self.characters_map,
            'characters_list': self.characters_list,
            'permutations': self.permutations,
            'permutations_inverse': self.permutations_inverse
        })
    
    def from_json(self, json_str) :
        """Load the Obfuscator object from a JSON string."""
        data = json.loads(json_str)
        self.key_name = data['key_name']
        self.characters_map = data['characters_map']
        self.characters_list = tuple(data['characters_list'])
        self.permutations = tuple(data['permutations'])
        self.permutations_inverse = tuple(data['permutations_inverse'])

