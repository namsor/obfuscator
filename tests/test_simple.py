# 
# to run all your tests when they follow the naming conventions, just run 
# 
# $ pytest
# 
# at the root of the repo
#
# see naming conventions for example here:
# https://docs.pytest.org/en/latest/goodpractices.html
# 


from obfuscator import Obfuscator

def test_helloworld_1():
    """
    Test the Obfuscator class with a simple example.
    """
    # corpus = alphabet
    corpus = "abcdefghijklmnopqrstuvwxyz"
    o = Obfuscator(corpus, iter_count=3, window_size=3)
    o_key =  o.to_json()
    print(o_key)
    clear = "hello world"
    encrypted = o.obfuscate(clear)
    decrypted = o.deobfuscate(encrypted) 
    print(f"test1 clear {clear} encrypted {encrypted} decrypted {decrypted}")
    assert encrypted != clear
    assert decrypted == clear

def test_json_2():
    """
    Test the Obfuscator class with JSON serialization.
    """
    # corpus = alphabet
    corpus = "abcdefghijklmnopqrstuvwxyz"
    o = Obfuscator(corpus, iter_count=3, window_size=3)
    o_key =  o.to_json()
    print(o_key)

    clear = "hello world"
    encrypted = o.obfuscate(clear)
    
    o2 = Obfuscator([])
    o2.from_json(o_key)

    decrypted2 = o2.deobfuscate(encrypted) 
    print(f"test2 clear {clear} o.encrypted {encrypted} o2.decrypted {decrypted2}")
    assert encrypted != clear
    assert decrypted2 == clear

