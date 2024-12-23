import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from ardgen import genA, genR, genD
from desolvertypes import Layer1HdrTypes, Layer2HdrTypes, Layer3HdrTypes, ServiceTypes
from desolvercore import Node, Edge, HasHeaderGen, TrafficModel, neinit

from desolvev3 import cdesolve
import sys
import requests

url = "http://47.94.74.58:8000/re/"
# url = "http://127.0.0.1:8000/re/"
seed = 42

pkts_type = 'exponential' # packet size type
inta_type = 'exponential' # interarrival time type

router_num = 4
host_num = 0

proto_stck = []
gamma = 0.05

edge_spds_r = np.array([1])  # edge rates for routers
dropprobs_r = np.array([0.1])

edge_spds_rh = np.array([np.inf])
dropprobs_rh = np.array([0])

avg_size = np.array([1])  # unit is bit, while the size of payload is byte.
pld_avg_size = avg_size / 8

start_time = np.float64(0)
end_time = np.float64(1e3)

attmt_assumpt = 'evenly'
topotype = 'tworouter'

A, Aspds, Adrps, ur, vh, router_num, host_num = genA(topotype, edge_spds_r, dropprobs_r, router_num,
    host_num, attmt_assumpt, edge_spds_rh, dropprobs_rh)

router_idcs = np.arange(1, router_num + 1)
node_num = router_num + host_num
host_idcs = np.arange(router_num + 1, node_num + 1)

u, v = np.nonzero(A)
Gh = nx.DiGraph()  # Create directed graph
for i in range(len(u)):
    Gh.add_edge(u[i] + 1, v[i] + 1)

edge_num = Gh.number_of_edges()
edge_idcs = range(1, edge_num + 1)

graph_mtx = np.zeros_like(A, dtype=int)
for idx, (u, v) in enumerate(Gh.edges):
    graph_mtx[u - 1, v - 1] = edge_idcs[idx]

fig_on = True
if fig_on:
    pos = nx.spectral_layout(Gh)  # you can choose a different layout if preferred
    nx.draw(Gh, pos, with_labels=True, node_color='lightblue', edge_color='gray',
            node_size=500, font_size=10, arrows=True)
    plt.show()

routalgo_assumpt = 'shortestpath'
node_idcs = np.concatenate([router_idcs, host_idcs])

R = genR(Gh, node_idcs, routalgo_assumpt)

demandtype = 'const'
D = genD(host_num, demandtype) # Generate the demand matrix
D = gamma * D  # Scale the demand matrix by gamma

nodes = [Node(idx) for idx in node_idcs]
edges = [Edge() for _ in edge_idcs]
nodes, edges = neinit(nodes, edges, router_num, node_idcs, Gh, graph_mtx, R, edge_idcs, Aspds, Adrps) # network element init

flow_num = np.count_nonzero(D)  # Number of non-zero elements in D (equivalent to nnz(D))

# Initialize gens and traf_mods as arrays of objects
gens = [HasHeaderGen() for _ in range(flow_num)]
traf_mods = [TrafficModel() for _ in range(flow_num)]
s, t = np.nonzero(D)

# Loop through each flow
for i in range(flow_num):
    sh = s[i] + router_num + 1  # source host index
    th = t[i] + router_num + 1  # target host index

    traf_mods[i] = TrafficModel(pkts_type, avg_size,
                                inta_type, D[s[i], t[i]],
                                ServiceTypes.IPerf, proto_stck, seed)

    gens[i] = HasHeaderGen(traf_mods[i], (i + 1), sh, th,
                           start_time, end_time)

    gens[i].allocate()
    outedgei_t = nodes[sh - 1].outedgei
    edges[edge_idcs.index(outedgei_t[0])].flow_objs.append(gens[i])
    edges[edge_idcs.index(outedgei_t[0])].fobj_num += 1

    if gens[i].ev_no > 0:
        print(f"Flow #{gens[i].flow_idx} will be running from {gens[i].start_time:.4f} sec "
              f"to {gens[i].end_time:.4f} sec with {gens[i].ev_no} packets.")

    seed += 1

Rr = R[:router_num, :router_num]
graph_mtx_r = graph_mtx[:router_num, :router_num]  # Equivalent to A(1:router_num, 1:router_num)

data = {
    "Rr": Rr.tolist(),
    "graph_mtx_r": graph_mtx_r.tolist(),
    "edge_num": edge_num,
}

try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    sorted_edges_r = response.json()
except requests.RequestException as e:
    print(f"An error occurred: {e} at the server side")
    sys.exit(1)

accd_edges = list((graph_mtx[vh - 1, ur - 1]))
exitd_edges = list((graph_mtx[ur - 1, vh - 1]))
sorted_edges = np.concatenate([accd_edges, sorted_edges_r, exitd_edges])

gens = cdesolve(edges, list(edge_idcs), edge_num, sorted_edges, nodes, graph_mtx, gens)

# gens = desolvev2(edges, edge_idcs, edge_num, sorted_edges, nodes, graph_mtx, gens)
print('THIS SIMULATION IS COMPLETED.')

for i in range(flow_num):    
    print(gens[i].soj_t)

print('end-to-end delay of flows were analyzed.')