import numpy as np
import networkx as nx
from mathx import calc_closest_factors, issymmetric


def genA(topotype, spds_r, drps_r, router_num,
         host_num, attmt_assumpt, spds_rh, drps_rh):


    if topotype == 'tworouter':
        u = 0
        v = 1
        router_num = 2
        
    elif topotype == 'triangle_ddlk':
        u = list(range(3))
        v = u[1:] + u[:1]
        router_num = 3

    elif topotype == "erdos_renyi":
        G = nx.erdos_renyi_graph(router_num, 0.2)
        At = nx.to_numpy_array(G)
        u, v = np.nonzero(At)

    elif topotype == "random_regular":
        G = nx.random_regular_graph(3, router_num)
        At = nx.to_numpy_array(G)
        u, v = np.nonzero(At)

    elif topotype == "grid":
        row, col = calc_closest_factors(router_num)
        G = nx.grid_2d_graph(row, col)
        At = nx.to_numpy_array(G)
        u, v = np.nonzero(At)
    else:
        return "invalid topotype."
    
    
    if host_num == 0:
        host_num = router_num
        
    node_num = router_num + host_num
    A = np.zeros((node_num, node_num), dtype=int)
    A[u, v] = 1

    if ~issymmetric(A):
        A = A + A.T

    A0 = np.triu(A)
    u, v = np.nonzero(A0)
    edgespds_r = spds_r[np.random.choice(len(spds_r), size=len(u))]
    edgedrps_r = drps_r[np.random.choice(len(drps_r), size=len(u))]

    Aspds = np.zeros((node_num, node_num))
    Adrps = np.zeros_like(Aspds)

    Aspds[u, v] = edgespds_r
    Adrps[u, v] = edgedrps_r

    Aspds[v, u] = edgespds_r  # bidirectional
    Adrps[v, u] = edgedrps_r  # bidirectional

    ur = np.array([], dtype=int)
    vh = np.array([], dtype=int)

    if attmt_assumpt == 'evenly':
        hostnumN = host_num // router_num  # Integer division
        hostnumE = host_num - hostnumN * (router_num - 1)  # For the last router
        host_idx1 = router_num

        for i in range(1, router_num + 1):  # Python is 0-indexed, MATLAB is 1-indexed
            host_idx0 = host_idx1 + 1

            if i != router_num:
                host_idx1 += hostnumN
                router_idcs_t = [i] * hostnumN  # Equivalent to repelem(i, hostnumN)
            else:
                host_idx1 += hostnumE
                router_idcs_t = [i] * hostnumE  # For the last router

            host_idcs_t = list(range(host_idx0, host_idx1 + 1))  # Generate indices

            ur = np.append(ur, router_idcs_t)
            vh = np.append(vh, host_idcs_t)

    # Get the corresponding values
    edgespds_rh = spds_rh[np.random.choice(len(spds_rh), len(ur))]
    edgedrps_rh = drps_rh[np.random.choice(len(drps_rh), len(ur))]

    A[ur - 1, vh - 1] = 1  # 1 offset
    A[vh - 1, ur - 1] = 1

    Aspds[ur - 1, vh - 1] = edgespds_rh
    Aspds[vh - 1, ur - 1] = edgespds_rh

    Adrps[ur - 1, vh - 1] = edgedrps_rh
    Adrps[vh - 1, ur - 1] = edgedrps_rh

    return A, Aspds, Adrps, ur, vh, router_num, host_num

def genR(G, node_idcs, routalgo_assumpt):
    node_num = len(node_idcs)
    R = np.zeros((node_num, node_num)).astype(np.int32)

    if routalgo_assumpt == 'shortestpath':
        for i in node_idcs:
            dests, nexthops = build_fwtbl(G, i)  # W should be defined elsewhere
            dests = [x - 1 for x in dests]
            R[i - 1, dests] = nexthops  # Assign next hops to corresponding destinations
    else:
        pass  # Handle other cases if needed
    return R


def genD(host_num, demandtype):
    D = np.zeros((host_num, host_num))  # Create a zero matrix

    if demandtype == 'const':
        D = np.diag(np.ones(host_num)) > 0  # Create a diagonal matrix
        D = np.double(~D)  # Invert the boolean matrix and convert to double

    return D

def build_fwtbl(graph, start_node):
    # Get shortest paths and the corresponding paths from start_node
    _, paths = nx.single_source_dijkstra(graph, start_node)
    next_hops = {}

    for dest in graph.nodes():
        if dest == start_node:
            continue
        # The shortest path to the destination
        path = paths[dest]
        # The next hop is the second node in the path
        next_hops[dest] = path[1]

    return list(next_hops.keys()), list(next_hops.values())
