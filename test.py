from hashcompare import Hash
from hashlib import sha1, sha256, blake2b, blake2s
from zlib import crc32
import time
import inspect
import numpy as np
import base58

x_range = [1,10,100,200,300,400,500,600,700,800, 900, 1000]

hash_mapper = [Hash(sha256(),"sha256"), Hash(sha1(),"sha1"), Hash(blake2b(),"blake2b"), Hash(blake2s(),"blake2s")]
hash_mapper = np.array(hash_mapper)

simulated_packet = "abcdefghij"
for idx, hash_f in enumerate(hash_mapper):

    for i in x_range:
        hash_mapper[idx].set_start(time.time())
        for j in range(Hash.NUM_OF_ROUNDS):
            packet = simulated_packet*i
            hash_f.update(packet.encode())
            hash_v = hash_f.digest()

        hash_mapper[idx].set_finish(time.time())

    print("{} {} performed {} operations in {} {} \n".format
        (idx, hash_mapper[idx].get_name(), Hash.NUM_OF_ROUNDS,  len(hash_mapper[idx].get_duration()), hash_mapper[idx].get_duration()))

