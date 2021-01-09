import numpy as np # per uint8, da valutare
import mmh3
from functools import partial
from core.shingleVector import ShingleVector


def get_hash_functions(k):
    hash = lambda seed, value: mmh3.hash(value, seed)
    hashes = [partial(hash, i) for i in range(0, k)]
    return hashes


def min_hash(shingle_set, hash_function):
    hashed_shingle_set = list(
        map(
            # converte le liste di tag in una stringa unica con separatore, poi ne calcola l'hash
            lambda shingle: hash_function(','.join(shingle.getContent())) %256, # da verificare hashing
            shingle_set
        )
    )
    # restituisce l'hash minimo tra tutti quelli degli shingle della pagina
    return min(hashed_shingle_set)

def create_shingle_vector(shingle_set):
    k_hash = get_hash_functions(8)
    shingle_vector = []
    for hash_function in k_hash:
        shingle_byte = min_hash(shingle_set, hash_function)
        assert shingle_byte >= 0 and shingle_byte <= 255, "shingle vector element should be a value between 0 and 255 (inclusive)"
        shingle_vector.append(shingle_byte)
    # ha senso restituire la webpage (uguale per tutti gli shingle), non il singolo shingle (scorrelato dal vector)
    return ShingleVector(shingle_set[0].webpage, shingle_vector)
