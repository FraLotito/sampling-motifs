from hypergraph import hypergraph
from utils import *
from loaders import *
import pickle
import random, time
from queue import Queue
from metrics import *
from samplemotifs import rand_motifs_3, rand_motifs_4, rand_motifs_5

def load(name):
    with open('{}'.format(str(name)), 'rb') as handle:
        b = pickle.load(handle)
        return b

def save(d, name):
    with open('{}'.format(str(name)), 'wb') as handle:
        pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)

N = 5
edges = load_high_school(N)
dataset = "hs_5"

#exact = load('results_ho/{}.pickle'.format(dataset))

S = 100

output = {}
"""

print("Observed")
if N == 3:
    output['motifs'] = rand_motifs_3(edges, S)
elif N == 4:
    output['motifs'] = rand_motifs_4(edges, S)
elif N == 5:
    output['motifs'] = rand_motifs_5(edges, S, verbose=True)

save(output, '{}_observed.pickle'.format(dataset))
"""

#print(output['motifs'])
#print(exact['motifs'])

STEPS = len(edges)*10

results = []

for i in range(2):
    print(i, "Conf")
    e1 = hypergraph(edges)
    e1.MH(label='stub', n_steps=STEPS)
    if N == 3:
        m1 = rand_motifs_3(e1.C, S)
    elif N == 4:
        m1 = rand_motifs_4(e1.C, S)
    elif N == 5:
        m1 = rand_motifs_5(e1.C, S, verbose=True)

    #null_model = e1.shuffle_edges(100)
    #m1 = count_motifs(null_model, N)
    results.append(m1)
    import random

    save(m1, '{}_conf_model_{}.pickle'.format(dataset, str(random.randint(0, 100000))))

output['config_model'] = results

#with open('results_ho/conference_{}.pickle'.format(N), 'wb') as handle:
#    pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)
#res = norm_vector(diff_sum(output['motifs'], output['config_model']))

#save(output, '{}_clustering.pickle'.format(dataset))
#res = norm_vector(diff_sum2(output['motifs'], output['config_model']))

#print(norm_vector(diff_sum(output['motifs'], output['config_model'])))
#print(norm_vector(diff_sum(exact['motifs'], exact['config_model'])))