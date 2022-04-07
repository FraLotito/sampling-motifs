import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 14})
sociodata = False

def get_avg(a):
    avg = []
    for v in a:
        avg.append(np.mean(v))
    return avg

def get_std(a):
    std = []
    for v in a:
        std.append(np.std(v))
    return std

def load_data():
    data = {}
    socio = ['ps', 'hs', 'EU']
    coauth = ['history', 'geology','dblp']
    if sociodata:
        names = socio
    else:
        names = coauth
    for d in names:
        data[d] = []
        f = open("{}_4_sampling_data.txt".format(d))
        lines = f.readlines()
        f.close()
        tmp = []
        for l in lines:
            l = l.split()
            if len(l) == 0:
                continue
            t = l[3][:len(l[3])-1]
            c = float(t)

            tmp.append(c)
            if len(tmp) == 4:
                data[d].append(tmp)
                tmp = []
    return data
            
data = load_data()
p = {}

for k in data:
    p[k] = {}
    p[k]['avg'] = get_avg(data[k])
    p[k]['std'] = get_std(data[k])
    print(p[k]['avg'])

if sociodata:
    l = [100, 250, 500, 1000, 2000]
else:
    l = [1000, 2500, 5000, 10000, 20000]

plt.xticks(range(5), labels=l)
plt.xlabel("S", fontsize=18)
plt.ylabel("execution time (s)", fontsize=18)

for k in p:
    plt.errorbar(x=range(len(p[k]['avg'])), y=p[k]['avg'], yerr=p[k]['std'], label=k, marker='o', capsize=3, capthick=0.5, ls='--')
import seaborn as sn
sn.despine()
plt.legend(frameon=False)
plt.tight_layout()
if sociodata:
    plt.savefig("time_socio.pdf")
else:
    plt.savefig("time_coauth.pdf")