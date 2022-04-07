import pickle
from utils import *

def load(name):
    with open('{}'.format(str(name)), 'rb') as handle:
        b = pickle.load(handle)
        return b

def save(d, name):
    with open('{}'.format(str(name)), 'wb') as handle:
        pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)

name = "history_5"
obs = load('{}_observed.pickle'.format(name))['motifs']

conf = []
his_conf_id = [15567, 24278, 37879, 41559, 44674, 53684, 77652, 80903, 91584, 99018]
hs_conf_id = [15773, 18596, 22146, 24504, 39126, 42578, 45741, 64597, 66516, 74399]

ids = []

if name == 'history_5':
    ids = his_conf_id
else:
    ids = hs_conf_id

for i in ids:
    tmp = '{}_conf_model_{}.pickle'.format(name, i)
    a = load(tmp)
    conf.append(a)

r = diff_sum2(obs, conf)
res = []
for i in r:
    res.append((i[1], i[0]))
res = list(sorted(res, reverse=True))[:5]
for r in res:
    print(r)