import wntr
import matplotlib.pyplot as plt

wn = wntr.network.WaterNetworkModel('networks/Net3.inp')
random_valve_layer = wntr.network.generate_valve_layer(wn, 'random', 40)
print(random_valve_layer.head())

ax = wntr.graphics.plot_valve_layer(wn, random_valve_layer, add_colorbar=False)

plt.show()