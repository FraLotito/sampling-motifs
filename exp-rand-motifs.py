from pip import main
from hypergraph import hypergraph
from utils import *
from loaders import *
import pickle
import random, time
from queue import Queue
from metrics import *

def load(name):
    with open('{}'.format(str(name)), 'rb') as handle:
        b = pickle.load(handle)
        return b

def split(edges):
    res = {}
    for e in edges:
        if len(e) in res:
            res[len(e)].append(e)
        else:
            res[len(e)] = [e] 
    return res

def max_card(motif):
    m = 0
    for e in motif:
        m = max(m, len(e))
    return m

def count_max_card(motif):
    m = max_card(motif)
    res = 0
    for e in motif:
        if len(e) == m:
            res+=1
    return res

def rand_motifs_3(edges, NS):
    N = 3
    mapping, labeling = generate_motifs(N)
    E = len(edges)
    NS = int(NS)

    T = {}
    graph = {}
    for e in edges:
        T[tuple(sorted(e))] = 1
        for e_i in e:
            if e_i in graph:
                graph[e_i].append(e)
            else:
                graph[e_i] = [e]

    def count_motif(nodes, avoid=False):
        nodes = tuple(sorted(tuple(nodes)))
        p_nodes = power_set(nodes)
        
        motif = []
        for edge in p_nodes:
            if len(edge) >= 2:
                edge = tuple(sorted(list(edge)))
                if edge in T:
                    motif.append(edge)
                    if len(edge) == 3 and avoid:
                        return

        m = {}
        idx = 1
        for i in nodes:
            m[i] = idx
            idx += 1

        labeled_motif = []
        for e in motif:
            new_e = []
            for node in e:
                new_e.append(m[node])
            new_e = tuple(sorted(new_e))
            labeled_motif.append(new_e)
        labeled_motif = tuple(sorted(labeled_motif))

        if labeled_motif in labeling:
            labeling[labeled_motif] += 1

    edges = list(edges)
    edges = split(edges)

    ns = {}
    ns[2] = int(0.25 * NS)
    ns[3] = int(0.75 * NS)
 
    sampled_edges = random.choices(edges[2], k=ns[2])

    for edge in sampled_edges:
        nodes = list(edge)
        for n in nodes:
            for e_i in graph[n]:
                tmp = list(nodes)
                tmp.extend(e_i)
                tmp = set(tmp)
                tmp = list(tmp)
                k = tuple(sorted(tmp))
                if len(tmp) == 3:
                    count_motif(tmp, True)

    sampled_edges = random.choices(edges[3], k=ns[3])
    for edge in sampled_edges:
        nodes = list(edge)
        count_motif(nodes)
    
    out = []

    for motif in mapping.keys():
        count = 0
        for label in mapping[motif]:
            count += labeling[label]
        if max_card(motif) == 3:
            p = int(count * (len(edges[3]) / ns[3]))
        else:
            p = int(count * (len(edges[2]) / (ns[2] * len(motif))))

        out.append((motif, p))

    out = list(sorted(out))

    D = {}
    for i in range(len(out)):
        D[i] = out[i][0]
    
    return out

def rand_motifs_4(edges, NS, verbose=False):
    N = 4
    E = len(edges)
    mapping, labeling = generate_motifs(N)

    T = {}
    graph = {}
    for e in edges:
        if len(e) <= N:
            T[tuple(sorted(e))] = 1
            for e_i in e:
                if e_i in graph:
                    graph[e_i].append(e)
                else:
                    graph[e_i] = [e]

    def count_motif(nodes, max_c):
        nodes = tuple(sorted(tuple(nodes)))
        p_nodes = power_set(nodes)
        
        motif = []
        for edge in p_nodes:
            if len(edge) >= 2:
                edge = tuple(sorted(list(edge)))
                if edge in T:
                    motif.append(edge)
                    if len(edge) > max_c:
                        return

        m = {}
        idx = 1
        for i in nodes:
            m[i] = idx
            idx += 1

        labeled_motif = []
        for e in motif:
            new_e = []
            for node in e:
                new_e.append(m[node])
            new_e = tuple(sorted(new_e))
            labeled_motif.append(new_e)
        labeled_motif = tuple(sorted(labeled_motif))

        if labeled_motif in labeling:
            labeling[labeled_motif] += 1
    
    edges = list(edges)
    edges = split(edges)

    ns = {}
    ns[2] = int(0.2 * NS)
    ns[3] = int(0.4 * NS)
    ns[4] = int(0.4 * NS)
    sampled_edges = random.choices(edges[2], k=ns[2])

    i = 0
    for edge in sampled_edges:
        i+=1
        if verbose:
            print("{} of {}".format(i, len(sampled_edges)))
        vis = {}
        nodes = list(edge)
        neigh = []
        for n in nodes:
            for e_i in graph[n]:
                neigh.append(e_i)
        for e_i in neigh:
            tmp = list(nodes)
            tmp.extend(e_i)
            tmp = list(set(tmp))
            k = tuple(sorted(tmp))
            if len(tmp) == 4 and k not in vis:
                count_motif(tmp, 2)
                vis[k] = 1
            else:
                neigh2 = []
                for n2 in tmp:
                    for e_i2 in graph[n2]:
                        neigh2.append(e_i2)
                for e_i2 in neigh2:
                    tmp2 = list(tmp)
                    tmp2.extend(e_i2)
                    tmp2 = list(set(tmp2))
                    k2 = tuple(sorted(tmp2))
                    if len(tmp2) == 4 and k2 not in vis:
                        count_motif(tmp2, 2)
                        vis[k2] = 1
    
    sampled_edges = random.choices(edges[3], k=ns[3])
    i = 0
    for edge in sampled_edges:
        i+=1
        if verbose:
            print("{} of {}".format(i, len(sampled_edges)))
        vis = {}
        nodes = list(edge)
        for n in nodes:
            for e_i in graph[n]:
                tmp = list(nodes)
                tmp.extend(e_i)
                tmp = list(set(tmp))
                k = tuple(sorted(tmp))
                if len(tmp) == 4 and k not in vis:
                    count_motif(tmp, 3)
                    vis[k] = 1

    sampled_edges = random.choices(edges[4], k=ns[4])
    i = 0
    for edge in sampled_edges:
        i+=1
        if verbose:
            print("{} of {}".format(i, len(sampled_edges)))
        nodes = list(edge)
        count_motif(nodes, 4)

    out = []

    for motif in mapping.keys():
        count = 0
        for label in mapping[motif]:
            count += labeling[label]
        
        p = int(count * (len(edges[max_card(motif)]) / (ns[max_card(motif)] * count_max_card(motif))))
        
        out.append((motif, p))

    out = list(sorted(out))
    
    return out

def rand_motifs_5(edges, NS, verbose=False):
    N = 5
    E = len(edges)
    labeling = {}

    def generate_all_relabelings(n, nodes):
        res = set()
        k = nodes
        relabeling_list = list(itertools.permutations([j for j in range(1, n + 1)]))
        for relabeling in relabeling_list:
            relabeling_i = relabel(k, relabeling)
            res.add((tuple(sorted(relabeling_i))))
        return res
    #mapping, labeling = generate_motifs(N)

    T = {}
    graph = {}
    for e in edges:
        if len(e) <= N:
            T[tuple(sorted(e))] = 1
            for e_i in e:
                if e_i in graph:
                    graph[e_i].append(e)
                else:
                    graph[e_i] = [e]

    def count_motif(nodes, max_c):
        nodes = tuple(sorted(tuple(nodes)))
        p_nodes = power_set(nodes)
        
        motif = []
        for edge in p_nodes:
            if len(edge) >= 2:
                edge = tuple(sorted(list(edge)))
                if edge in T:
                    motif.append(edge)
                    if len(edge) > max_c:
                        return

        m = {}
        idx = 1
        for i in nodes:
            m[i] = idx
            idx += 1

        labeled_motif = []
        for e in motif:
            new_e = []
            for node in e:
                new_e.append(m[node])
            new_e = tuple(sorted(new_e))
            labeled_motif.append(new_e)
        labeled_motif = tuple(sorted(labeled_motif))

        if labeled_motif in labeling:
            labeling[labeled_motif] += 1
        else:
            labeling[labeled_motif] = 1
    
    edges = list(edges)
    edges = split(edges)

    ns = {}
    ns[2] = int(0.1 * NS)
    ns[3] = int(0.2 * NS)
    ns[4] = int(0.3 * NS)
    ns[5] = int(0.4 * NS)
    sampled_edges = random.choices(edges[2], k=ns[2])

    i = 0
    for edge in sampled_edges:
        i+=1
        if verbose:
            print("{} of {}".format(i, len(sampled_edges)))
        vis = {}
        nodes = list(edge)
        neigh = []
        for n in nodes:
            for e_i in graph[n]:
                neigh.append(e_i)
        for e_i in neigh:
            tmp = list(nodes)
            tmp.extend(e_i)
            tmp = list(set(tmp))
            k = tuple(sorted(tmp))
            if len(tmp) == 5 and k not in vis:
                count_motif(tmp, 2)
                vis[k] = 1
            else:
                neigh2 = []
                for n2 in tmp:
                    for e_i2 in graph[n2]:
                        neigh2.append(e_i2)
                for e_i2 in neigh2:
                    tmp2 = list(tmp)
                    tmp2.extend(e_i2)
                    tmp2 = list(set(tmp2))
                    k2 = tuple(sorted(tmp2))
                    if len(tmp2) == 5 and k2 not in vis:
                        count_motif(tmp2, 2)
                        vis[k2] = 1
                    else:
                        neigh3 = []
                        for n3 in tmp2:
                            for e_i3 in graph[n3]:
                                neigh3.append(e_i3)
                        for e_i3 in neigh3:
                            tmp3 = list(tmp2)
                            tmp3.extend(e_i3)
                            tmp3 = list(set(tmp3))
                            k3 = tuple(sorted(tmp3))
                            if len(tmp2) == 5 and k3 not in vis:
                                count_motif(tmp3, 2)
                                vis[k3] = 1

    sampled_edges = random.choices(edges[3], k=ns[3])
    i = 0
    for edge in sampled_edges:
        i+=1
        if verbose:
            print("{} of {}".format(i, len(sampled_edges)))
        vis = {}
        nodes = list(edge)
        neigh = []
        for n in nodes:
            for e_i in graph[n]:
                neigh.append(e_i)
        for e_i in neigh:
            tmp = list(nodes)
            tmp.extend(e_i)
            tmp = list(set(tmp))
            k = tuple(sorted(tmp))
            if len(tmp) == 5 and k not in vis:
                count_motif(tmp, 3)
                vis[k] = 1
            else:
                neigh2 = []
                for n2 in tmp:
                    for e_i2 in graph[n2]:
                        neigh2.append(e_i2)
                for e_i2 in neigh2:
                    tmp2 = list(tmp)
                    tmp2.extend(e_i2)
                    tmp2 = list(set(tmp2))
                    k2 = tuple(sorted(tmp2))
                    if len(tmp2) == 5 and k2 not in vis:
                        count_motif(tmp2, 3)
                        vis[k2] = 1
    
    sampled_edges = random.choices(edges[4], k=ns[4])
    i = 0
    for edge in sampled_edges:
        i+=1
        if verbose:
            print("{} of {}".format(i, len(sampled_edges)))
        vis = {}
        nodes = list(edge)
        for n in nodes:
            for e_i in graph[n]:
                tmp = list(nodes)
                tmp.extend(e_i)
                tmp = list(set(tmp))
                k = tuple(sorted(tmp))
                if len(tmp) == 5 and k not in vis:
                    count_motif(tmp, 4)
                    vis[k] = 1

    sampled_edges = random.choices(edges[5], k=ns[5])
    i = 0
    for edge in sampled_edges:
        i+=1
        if verbose:
            print("{} of {}".format(i, len(sampled_edges)))
        nodes = list(edge)
        count_motif(nodes, 5)

    out = {}
    vis_m = {}

    for motif in labeling.keys():
        count = 0

        if motif not in vis_m:
            all_labels = generate_all_relabelings(N, motif)
            for label in all_labels:
                vis_m[label] = True
                if label in labeling.keys():
                    count += labeling[label]
            
            p = int(count * (len(edges[max_card(motif)]) / (ns[max_card(motif)] * count_max_card(motif))))
        
            out[motif] = p
    
    return out

if __name__ == "__main__":
    N = 4
    edges = load_DBLP(N)
    dataset = "dblp_4"

    exact = load('results_ho/{}.pickle'.format(dataset))['motifs']
    f = open("{}_sampling_data.txt".format(dataset), 'w+')

    R = 0.01

    for p in [1000, 2500, 5000, 10000, 20000]:
        for i in range(1, 5):
            print(p, i)
            start = time.time()
            output = {}

            if N == 3:
                output['motifs'] = rand_motifs_3(edges, p)
            elif N == 4:
                output['motifs'] = rand_motifs_4(edges, p)
            elif N == 5:
                output['motifs'] = rand_motifs_5(edges, len(edges) * p, N)

            #print([i[1] for i in output['motifs']])
            est = output['motifs']
            end = time.time()
            print("p: {}, TIME: {}\n".format(p, end - start))
            print(max_relative_error(exact, est), mean_relative_error(exact, est), kendall(exact, est))
            
            f.write("p: {}, time: {}, corr: {}\n".format(p, end - start, kendall(exact, est)))
    f.close()
    exit(0)
    #print([i[1] for i in output['motifs']])

    #for c in output['motifs']:
    #    if c[1] > 0:
    #        print(c)

    """
    STEPS = len(edges)*10

    results = []

    for i in range(10):
        e1 = hypergraph(edges)
        e1.MH(label='stub', n_steps=STEPS)
        if N == 3:
            m1 = rand_motifs_3(e1.C, len(e1.C) * p)
        elif N == 4:
            m1 = rand_motifs_4(e1.C, len(e1.C) * p)

        #null_model = e1.shuffle_edges(100)
        #m1 = count_motifs(null_model, N)
        results.append(m1)

    output['config_model'] = results

    #with open('results_ho/conference_{}.pickle'.format(N), 'wb') as handle:
    #    pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)
    res = norm_vector(diff_sum(output['motifs'], output['config_model']))
    print(res)
    """