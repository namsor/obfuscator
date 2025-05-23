# corpustools and obfuscator
This approach allows to train character level embeddings on an obfuscated corpus, ie. corpus where the character substitutions are "secret". This may not be robust on an adversarial server, but helps keep training data reasonably private. Also, it makes reverse engineering of the trained embedding model slightly more complex. The overhead to obfuscate input data for the embedding model is minimal. 

## install
pip install git+https://github.com/namsor/obfuscator

## corpustools usage
corpustools 'C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf.txt' --gen_key --max_lines 10000000 --key_file 'C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf_key.json' --key_name namsorv3_proto0 --flair_file 'C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf_key_flair'

corpustools 'C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf.txt' --obfuscate --key_file 'C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf_key.json' --output_file 'C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf_obf.txt'

corpustools 'C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf_obf.txt' --deobfuscate --key_file 'C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf_key.json' --output_file 'C:/Sync/namsor Dropbox/NamSorV3/2_Prototyping/CAIRNN_Flair/full_corpus/corpus_full_untagged_shuf_deobf.txt'

