from hashlib import sha1, sha256, blake2b, blake2s
from blake3 import blake3, KEY_LEN, OUT_LEN
from zlib import crc32
import time
import inspect
import numpy as np

class Hash(object):
    NUM_OF_ROUNDS = 10000

    def __init__(self, hash_fuction, name):
        self.duration = []
        self.hash_fuction = hash_fuction
        self.name = name

    def set_start(self, start):
        self.start = start

    def set_finish(self, finish):
        self.finish = finish
        self.duration.append(self.finish - self.start)

    def get_duration(self):
        return self.duration

    def get_name(self):
        return self.name

    def bytes_to_float(self, b):
        return float(crc32(b) & 0xffffffff) / 2**32

    def update(self, data, args=[]):
        self.hash_fuction.update(data)
        for item in args:
            self.hash_fuction.update(item)

    def digest(self):
        return self.hash_fuction.digest()

"""
preprocessing such as 
1. 
2. 
"""
x_range = [1,10,100,200,300,400,500,600,700,800, 900, 1000]

hash_mapper = [Hash(sha256(), "sha256"), Hash(sha1(), "sha1"), Hash(blake2b(), "blake2b"), Hash(blake2s(), "blake2s"), Hash(blake3(), "blake3")]
hash_mapper = np.array(hash_mapper)

simulated_packet = "abcdefghij"
packet = []
for weight in x_range:
    packet.append(simulated_packet * weight)

for idx, hash_f in enumerate(hash_mapper):

    for i in range(len(x_range)):
        hash_mapper[idx].set_start(time.time())
        for j in range(Hash.NUM_OF_ROUNDS):
            # packet = simulated_packet*i
            hash_f.update(packet[i].encode())
            hash_v = hash_f.digest()

        hash_mapper[idx].set_finish(time.time())

    print("{} {} performed {} operations in {} {} \n".format
          (idx, hash_mapper[idx].get_name(), Hash.NUM_OF_ROUNDS, len(hash_mapper[idx].get_duration()),
           hash_mapper[idx].get_duration()))
default_duration = np.array(hash_mapper[0].get_duration())

import pandas as pd
import matplotlib.pyplot as plt
default_duration = pd.DataFrame(default_duration)

plot_result = {}
relative_performance = {}
for idx, hash_f in enumerate(hash_mapper):
    hash_mapper[idx].duration = pd.DataFrame(hash_mapper[idx].get_duration())
    hash_mapper[idx].duration.name = hash_mapper[idx].get_name()

    relative_performance.update({idx: hash_mapper[idx].get_duration()/default_duration})
    #print(relative_performance[idx])
    alist = []
    for item in relative_performance[idx].values:
        alist.append(item)
        #nlist = np.asanyarray(alist).astype(float)
        plot_result.update({hash_mapper[idx].get_name():alist})

plot_result =  pd.DataFrame(plot_result, index=x_range)
plot_result.sha256 = plot_result.sha256.astype(float)
plot_result.sha1 = plot_result.sha1.astype(float)
plot_result.blake2b = plot_result.blake2b.astype(float)
plot_result.blake2s = plot_result.blake2s.astype(float)
plot_result.blake3 = plot_result.blake3.astype(float)

ax = plot_result.plot()
ax.set_xlabel("The Size of Packets")
ax.set_ylabel("Relative Time")
ax.legend(loc='center right')
plt.show()

# Make Jupyter notebook
# Make RSA-SHA256 Encryption
# Make packet outside of time zone
