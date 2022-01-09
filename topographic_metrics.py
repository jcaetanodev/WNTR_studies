import networkx as nx
import wntr

wn = wntr.network.WaterNetworkModel('networks/Net3.inp')
G = wn.get_graph() # directed multigraph
uG = G.to_undirected() # undirected multigraph
sG = nx.Graph(uG) # undirected simple graph (single edge between two nodes)


# Node degree and terminal nodes
node_degree = G.degree()
terminal_nodes = wntr.metrics.terminal_nodes(G)

# Link density
link_density = nx.density(G)

# Diameter and eccentricity
diameter = nx.diameter(uG)
eccentricity = nx.eccentricity(uG)

# Betweenness centrality and central point dominance
betweenness_centrality = nx.betweenness_centrality(sG)
central_point_dominance = wntr.metrics.central_point_dominance(G)

# Closeness centrality
closeness_centrality = nx.closeness_centrality(G)

# Articulation points and bridges
articulation_points = list(nx.articulation_points(uG))
bridges = wntr.metrics.bridges(G)

# Shortest path length between all nodes and average sorthest path length
shortest_path_length = nx.shortest_path_length(uG)
ave_shortest_path_length = nx.average_shortest_path_length(uG)

# Paths between two nodes in a weighted graph, where the graph is weighted by 
# flow direction from a hydraulic simulation
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

flowrate = results.link['flowrate'].iloc[-1,:] # flowrate from the last timestep
G = wn.get_graph(link_weight=flowrate, modify_direction=True)
all_paths = nx.all_simple_paths(G, '119', '193')

# Valve segmentation, where each valve is defined by a node and link pair
valve_layer = wntr.network.generate_valve_layer(wn, 'random', 40)
node_segments, link_segments, segment_size = wntr.metrics.valve_segments(G, valve_layer)

# Valve segment attributes
average_expected_demand = wntr.metrics.average_expected_demand(wn)
link_lengths = wn.query_link_attribute('length')
valve_attributes = wntr.metrics.valve_segment_attributes(valve_layer, 
                    node_segments, 
                    link_segments,
                    average_expected_demand,
                    link_lengths
                    )