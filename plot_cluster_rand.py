import pickle
import pandas as pd
import matplotlib.pyplot as plt
from utils import *

plt.rcParams.update({'font.size': 14})


def load(name):
    with open('{}'.format(str(name)), 'rb') as handle:
        b = pickle.load(handle)
        return b

def save(d, name):
    with open('{}'.format(str(name)), 'wb') as handle:
        pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_data():
    data = {}
    for d in ['ps', 'hs', 'EU', 'history', 'geology', 'dblp']:
        data[d] = load("{}_4_clustering.pickle".format(d))
    return data

scores = load_data()

import seaborn as sn
import matplotlib.pyplot as plt

for k in scores:
    occ = scores[k]['motifs']
    conf = scores[k]['config_model']
    scores[k] = norm_vector(diff_sum(occ, conf))

df = pd.DataFrame(scores, columns=list(scores.keys()))
corr = df.corr()
sn.heatmap(corr)

plt.tight_layout()
#plt.show()
plt.savefig("cluster-rand.pdf")