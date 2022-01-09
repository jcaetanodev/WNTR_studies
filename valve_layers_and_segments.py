import wntr
import matplotlib.pyplot as plt

wn = wntr.network.WaterNetworkModel('networks/Net3.inp')
valve_layer = wntr.network.generate_valve_layer(wn, 'strategic', 2, seed=123)

G = wn.get_graph()

node_segments, link_segments, seg_sizes = wntr.metrics.topographic.valve_segments(G, valve_layer)

N = seg_sizes.shape[0]

cmap = wntr.graphics.random_colormap(N) # random color map helps view segments

ax = wntr.graphics.plot_network(wn, 
                                link_attribute=link_segments, 
                                node_size=0, 
                                link_width=2,
                                node_range=[0,N], 
                                link_range=[0,N], 
                                node_cmap=cmap, 
                                link_cmap=cmap,
                                link_colorbar_label='Segment')

ax = wntr.graphics.plot_valve_layer(wn, valve_layer, add_colorbar=False, include_network=False, ax=ax)

print(link_segments.head())

plt.show()