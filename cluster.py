import pickle
from typing import Type
import numpy as np
from pandas.core.algorithms import diff
from utils import avg, diff_sum, z_score, count, norm_vector
import sys

import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 12

ADDED_DATA = True


H_O = True
PACS_OPT = True

if H_O:
    path = 'results_ho'
else:
    path = 'results_classic'

try:
    N = int(sys.argv[1])
except:
    print("N = 3 by deafult")
    N = 3
assert(N == 3 or N == 4)

d = {}

datasets = ['gene', 'ndcclasses', 'ndcsub', 'workplace', 'hs', 'ps', 'hospital', 'justice', 'wiki', 'conference', 'baboons', 'enron', 'EU', 'dblp', 'history', 'geology']

for data in datasets:
    try:
        if data == 'baboons':
            with open('{}/{}_{}.pickle'.format(path, 'babbuini', N), 'rb') as handle:

                d[data] = pickle.load(handle)
                try:
                    import os
                    dir_name = 'additional_data/{}_{}'.format(data, N)
                    for filename in os.listdir(dir_name):
                        add_data = pickle.load(open(filename, 'rb'))
                        d[data]['config_model'].extend(add_data)
                except:
                    print("FAIL {}".format(data))

                d[data]['score'] = norm_vector(diff_sum(d[data]['motifs'], d[data]['config_model']))
                #d[data]['score'] = norm_vector(z_score(d[data]['motifs'], d[data]['config_model']))
                #d[data]['score'] = count(d[data]['motifs'])
        else:

            with open('{}/{}_{}.pickle'.format(path, data, N), 'rb') as handle:
                print(data)
                try:
                    d[data] = pickle.load(handle)
                except:
                    print("FAIL ORIGINAL DATA")
                print("Original", len(d[data]['config_model']))
                try:
                    import os
                    if not ADDED_DATA:
                        raise TypeError
                    dir_name = 'additional_data/{}_{}/'.format(data, N)
                    for filename in os.listdir(dir_name):
                        add_data = pickle.load(open(dir_name + filename, 'rb'))
                        d[data]['config_model'].append(add_data)
                except:
                    print("FAIL {}".format(data))
                print("Added", len(d[data]['config_model']))

                a = diff_sum(d[data]['motifs'], d[data]['config_model'])

                d[data]['score'] = norm_vector(a)
                #d[data]['score'] = norm_vector(z_score(d[data]['motifs'], d[data]['config_model']))
                #d[data]['score'] = count(d[data]['motifs'])
    except:
        pass

scores = {}
for k in d:
    scores[k] = list(d[k]['score'])

datasets = ['gene', 'ndcclasses', 'ndcsub', 'workplace', 'hs', 'ps', 'hospital', 'justice', 'wiki', 'conference', 'baboons', 'enron', 'EU', 'dblp', 'history', 'geology']

if PACS_OPT:
    PACS = {}
    for n in range(10):
        try:
            with open('single_PACS/PACS{}_{}.pickle'.format(n, N), 'rb') as handle:
                k = 'PACS{}'.format(n)
                PACS[k] = pickle.load(handle)
                #PACS[k]['score'] = norm_vector(diff_sum(PACS[k]['motifs'], PACS[k]['config_model']))
                #d[data]['score'] = norm_vector(z_score(d[data]['motifs'], d[data]['config_model']))
                #d[data]['score'] = count(d[data]['motifs'])
                try:
                    import os
                    dir_name = 'additional_data/{}_{}/'.format(k, N)
                    
                    for filename in os.listdir(dir_name):
                        add_data = pickle.load(open(dir_name + filename, 'rb'))
                        PACS[k]['config_model'].append(add_data)
                except:
                    print("FAIL {}".format("PACS_{}".format(n)))

                PACS[k]['score'] = norm_vector(diff_sum(PACS[k]['motifs'], PACS[k]['config_model']))
        
        except:
            pass
    for k in PACS.keys():
        scores[k] = list(PACS[k]['score'])

import pandas as pd
#print(pd.DataFrame(scores).corr())

bio = [0, 1, 2]
socio = [3, 4, 5, 6,7, 8, 9, 10]
tech = [11, 12]

df = pd.DataFrame(scores, columns=list(scores.keys()))
corr = df.corr()
print(corr)

import seaborn as sn
import matplotlib.pyplot as plt

#corr = cluster_corr(corr)
#print(df)
row_colors = []

i = 0
for k in scores.keys():
    if i in bio:
        row_colors.append('blue')
    elif i in socio:
        row_colors.append("red")
    elif i in tech:
        row_colors.append("orange")
    else:
        row_colors.append("purple")
    i+=1


c = sn.clustermap(corr, annot=False, method="complete", cmap="vlag", center=0, vmin=-1, vmax=1, row_colors=row_colors, xticklabels=False)
c.ax_col_dendrogram.remove()
c.cax.set_visible(False)

plt.title("Motifs size {}".format(N))
plt.tight_layout()
#plt.show()
plt.savefig("cluster-{}.pdf".format(N))

"""
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy  import maxdists
plt.figure()
z = hierarchy.linkage(corr, 'complete')
print(z)
"""

