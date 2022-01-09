import wntr
import matplotlib.pyplot as plt

wn = wntr.network.WaterNetworkModel('networks/Net3.inp')

wn.add_curve('Curve', 'VOLUME', [
            (1,  0),
            (2,  60),
            (3,  188),
            (4,  372),
            (5,  596),
            (6,  848),
            (7,  1114),
            (8,  1379),
            (9,  1631),
            (10, 1856),
            (11, 2039),
            (12, 2168),
            (13, 2228)])
tank = wn.get_node('2')
tank.vol_curve_name = 'Curve'
ax = wntr.graphics.plot_tank_volume_curve(tank)

plt.show()