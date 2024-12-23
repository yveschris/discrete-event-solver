import numpy as np
from desolvertypes import DropTypes
from poisson_fixed_time import poisson_fixed_time
import networkx as nx

class Edge:
    def __init__(self, idx = 0, speed = 0, dropprob=0, edge_type=None):
        self.edge_type = None
        self.idx = idx
        self.speed = speed
        self.dropprob = dropprob
        self.edge_type = edge_type  # Edge type
        self.flow_objs = []  # List to hold flow objects
        self.fobj_num = 0


class Node:
    def __init__(self, idx = None, node_type = None):
        self.idx = idx
        self.node_type = node_type
        self.neigh = []  # List of neighbors
        self.outedgei = []  # List for outgoing edges
        self.inedgei = []  # List for incoming edges

        # Routing related properties
        self.nexthops = []  # Buffer relative indices w.r.t neighbors
        self.dests = []  # Routing table; destinations

        self.nw_prop = None  # Placeholder for network properties

    def addEntriesBasedOnDests(self, dests, nh_idcs):

        for i in range(len(dests)):
            if dests[i] not in self.dests:
                # Destination not in the list; add it
                self.dests.append(dests[i])
                self.nexthops.append(self.neigh.index(nh_idcs[i]))  # Add index of the neighbor
            else:
                # Destination already exists; update the corresponding next hop
                idx_t = self.dests.index(dests[i])  # Get index of the existing destination
                self.nexthops[idx_t] = self.neigh.index(nh_idcs[i])  # Update the next hop index

class TrafficModel:
    def __init__(self, *args):
        if len(args) != 0:
            self.pktsize_type = args[0]
            self.avg_size = args[1]
            self.avg_pldsize = self.avg_size / 8

            self.interarriv_type = args[2]
            self.arrivr = args[3]

            self.serv_type = args[4]
            self.proto_stck = args[5]
            self.seed = args[6]

    def generate_RVs(self, start_time, sim_time):
        iav = 1 / self.arrivr

        if self.interarriv_type == 'constant':
            ev_no = int(np.floor((sim_time - start_time) / iav)) + 1
            createdt = np.arange(start_time, sim_time + iav, iav)

        elif self.interarriv_type == 'exponential':
            if sim_time:           
                createdt = poisson_fixed_time(start_time, sim_time, self.seed, self.arrivr)
                ev_no = len(createdt)
            else:
                createdt = np.cumsum((1 / iav) * np.random.exponential(1, ev_no)) + start_time

        else:
            ev_no = 0
            createdt = np.array([])

        if self.pktsize_type == 'constant':
            z = np.full(ev_no, self.avg_pldsize)

        elif self.pktsize_type == 'exponential':
            z = np.random.exponential(self.avg_pldsize, ev_no)

        else:
            z = np.array([])

        return z, createdt, ev_no


class EventFlow:
    def __init__(self, flow_idx, src, dest, soj_t, sizes, created, sent, seqs, ev_no, start_time, end_time):
        # Initialize the properties
        self.flow_idx = flow_idx  # Flow index
        self.src = src  # Source index
        self.dest = dest  # Destination index
        self.soj_t = soj_t  # Sojourn time

        # These six parameters are key concepts for the light speed simulator
        self.sizes = sizes  # Size array
        self.created = created  # Creation time
        self.sent = sent  # Sent time
        self.seqs = seqs  # Sequence numbers
        self.ev_no = ev_no  # Event numbers (vector)

        # Start and end time of the event
        self.start_time = start_time
        self.end_time = end_time


class HasHeaderGen(EventFlow):
    def __init__(self, *args):
        if len(args) == 0:
            return
        else:
            self.traf_mod = args[0]  # Traffic model object
            self.flow_idx = args[1]
            self.src = args[2]
            self.dest = args[3]

            self.start_time = args[4]
            self.end_time = args[5]

            self.ev_no = 0  # Number of events initially set to 0

    def allocate(self):

        # Call function to calculate the header size
        hdr_size = calc_hdr_size(self.traf_mod.proto_stck)

        # Generate payload sizes and events using traffic model's method
        self.pld_sizes, self.created, self.ev_no = self.traf_mod.generate_RVs(self.start_time, self.end_time)

        # Update drop_marks based on the number of events
        self.drop_marks = np.full(self.ev_no, DropTypes.NoDrop)

        # Calculate total packet sizes (payload size + header size), in bits
        self.sizes = (self.pld_sizes + hdr_size) * 8

        # Sent times equal to created times
        self.sent = self.created

        # Sequence numbers from 1 to ev_no
        self.seqs = np.arange(1, self.ev_no + 1)


def extract_from_flow_objs(flow_objs, flow_num, remai_v):
    # Initialize empty lists for outputs
    arriv_c = [None] * flow_num
    sizes_c = [None] * flow_num
    indv_fi_c = [None] * flow_num
    indv_fd_c = [None] * flow_num

    for i in range(flow_num):
        if remai_v[i] != 0:
            arriv_c[i] = flow_objs[i].created
            sizes_c[i] = flow_objs[i].sizes
            indv_fi_c[i] = [flow_objs[i].flow_idx] * remai_v[i]
            indv_fd_c[i] = [flow_objs[i].dest] * remai_v[i]

    return arriv_c, sizes_c, indv_fi_c, indv_fd_c


# network element init
def neinit(nodes, edges, router_num, node_idcs, Gh, graph_mtx, R, edge_idcs, Aspds, Adrps):
    
    node_num = Gh.number_of_nodes()
    for i in range(node_num):

        if i < router_num:
            nodes[i].node_type = 'router'
        else:
            nodes[i].node_type = 'host'

        for (u, v) in Gh.out_edges(nodes[i].idx):
            nodes[i].neigh.append(v)
            nodes[i].outedgei.append(graph_mtx[u - 1, v - 1])

        for (u, v) in Gh.in_edges(nodes[i].idx):
            nodes[i].inedgei.append(graph_mtx[u - 1, v - 1])

        node_idcs_t = node_idcs          # Create a copy of the node indices
        node_idcs_t = np.delete(node_idcs_t, i)  # Remove the current index

        nh_t = R[i, :]                   # Get the next hops for the current node
        nh_t = np.delete(nh_t, i)                  # Remove the current hop

        # Update the routing table for the current node
        nodes[i].addEntriesBasedOnDests(node_idcs_t, nh_t)

    print('routers and hosts were instantiated.')
    
    for idx, (u, v) in enumerate(Gh.edges):
        edges[idx] = Edge(edge_idcs[idx], Aspds[u - 1, v - 1], Adrps[u - 1, v - 1], 'NwIntf')

    print('Edges were instantiated.')
    return nodes, edges

def calc_hdr_size(proto_stck):
    hdr_size = 0
    for proto in proto_stck:
        hdr_size += proto
    return hdr_size

    