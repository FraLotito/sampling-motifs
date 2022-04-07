# Exact and sampling methods for mining higher-order motifs in large hypergraphs

This code implements the different algorithms for higher-order motif analysis proposed in the paper submitted at ECMLPKDD2022.

## Abstract

Network motifs are patterns of interactions occurring among a small set of nodes in a graph. They highlight fundamental aspects of the interplay between the topology and the dynamics of complex networks and have been proved to have a wide range of real-world applications. Motif analysis has been extended to a variety of network models that allow for a richer description of the interactions of a system, including weighted, temporal, multilayer, and, more recently, higher-order networks. Generalizing network motifs to capture patterns of group interactions is not only interesting from the fundamental perspective of understanding complex systems but also proposes unprecedented computational challenges. In this work, we focus on the problem of counting occurrences of sub-hypergraph patterns in a potentially huge empirical higher-order network. We show that, by directly exploiting higher-order structures, we dramatically speed up the counting process compared to applying traditional data mining techniques for network motifs. Moreover, by including hyperedge sampling techniques computational complexity is further improved at the cost of minimal errors in the estimation of motif frequency. We evaluate our algorithms on several social real-world datasets describing face-to-face interactions, co-authorship and human communication. We show that our approximated algorithm not only allows to speed up the performance, but also to extract larger higher-order motifs beyond the computational limits of an exact approach.

## Code organization
* ```exp-rand-motifs.py``` contains the implementation of the sampling algorithm proposed in the paper
* ```motifs.py``` contains the implementation of the baseline algorithm proposed in the paper
* ```motif2.py``` contains the implementation of the efficient algorithm proposed in the paper
* ```utils.py``` contains some useful functions
* ```loaders.py``` contains the loader for the datasets (see section below)
* ```hypergraph.py``` contains the implementation of a data structure for hypergraphs in Python and the configuration model for hypergraphs proposed by [Phil Chodrow](https://github.com/PhilChodrow)

NB: as of now there are other files that are useful for paper visualizations and analyses, they will be removed at publication time.

## Datasets
Please download the datasets [here](https://drive.google.com/file/d/1uFaftX_hqjTiBt2SZ_6fbggYG9ySK3Ss/view?usp=sharing) and extract the archive inside the main directory.

## How to use custom datasets
If you wish to perform higher-order motif analysis on your own datasets, you should implement a custom ```loader``` function. This function should return a set of tuples. Each tuple represents an hyperedge, and will contain the ids of the nodes involved in a group interactions.  

## How to perform higher-order motif analysis
If you wish to experiment with the code, you can run analysis setting up the parameter ```N``` in the code, which specifies the order of the motifs to use for the analysis. At the moment, the only feasible orders for exact algorithms are ```N=3``` and ```N=4```. The parameter ```ROUNDS``` specifies the number of samples from the configuration model. Keep in mind that ```ROUNDS``` can heavily affect the performance. A value between 10 and 20 already gives reliable results. For the sampling algorithm, the parameter ```S``` controls the number of hyperedges to sample from the hypergraphs. Values of ```S``` between 1000 and 10000 give good results for co-authorship data, values of ```S``` between 100 and 1000 give good results for social data. The sampling algorithm allows for the analysis of motifs of size ```N=3```, ```N=4``` and ```N=5```.

## Acknowledgments
We thank [Phil Chodrow](https://github.com/PhilChodrow) for the code in the file ```hypergraph.py```



