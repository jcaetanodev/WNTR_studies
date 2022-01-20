import wntr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
import datetime


fn = datetime.datetime.now().strftime("%H%M_%d%m%y")

wn = wntr.network.WaterNetworkModel('networks/vilamoura_verao_zmc_bomba_quintinhas.inp')
# Adjust simulation options for criticality analyses
# analysis_end_time = 24*3600 
# wn.options.time.duration = analysis_end_time
wn.options.hydraulic.demand_model = 'PDD'
wn.options.hydraulic.required_pressure = 10 # alterar 30 m.c.a 
wn.options.hydraulic.minimum_pressure = 0 # alterar 5 m.c.a

reservoir_names = wn.reservoir_name_list
tank_names = wn.tank_name_list
reservoir_names.extend(tank_names)

################## Segments ##################
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

#plt.show()

length = wn.query_link_attribute('length',np.greater, 0,link_type=wntr.network.model.Pipe)    
diameter = wn.query_link_attribute('diameter',np.greater, 0,link_type=wntr.network.model.Pipe)    

dataframe = pd.concat([length, diameter, link_segments], axis=1, join='inner', ignore_index=False) 

################## Segments ##################

# Run a preliminary simulation to determine if junctions drop below the 
# pressure threshold during normal conditions
sim = wntr.sim.WNTRSimulator(wn)
results = sim.run_sim()

node_demand=results.node['demand']
demands = results.node['demand'].drop(reservoir_names, axis=1)
demand_at_inlet=(demands*3600).sum().sum()


# Run the criticality analysis, closing one pipe for each simulation
junctions_impacted = {} 

list_of_segments = set(dataframe[2])

print(list_of_segments)

for segment in list_of_segments:
    for index, row in dataframe.iterrows():
        print(f'Segment: {segment} of {len(list_of_segments)} and Pipe: {index}')
        wn.reset_initial_values()        
        if segment == row[2]:
            # print(f'close pipe {index} to belong on segment {segment}')
            # Add a control to close the pipe
            pipe = wn.get_link(index)      
            act = wntr.network.controls.ControlAction(pipe, 'status',wntr.network.LinkStatus.Closed)
            #cond = wntr.network.controls.SimTimeCondition(wn, "=", '23:00:00')
            cond = wntr.network.controls.TimeOfDayCondition(wn, 'after', '00:00:00')
            ctrl = wntr.network.controls.Control(cond, act)
            wn.add_control('close pipe ' + index, ctrl)
    wn.write_inpfile('networks/Inp_close_segment_'+'_'+fn+'.inp')

    # Run a PDD simulation
    sim = wntr.sim.WNTRSimulator(wn)
    results = sim.run_sim()

    demands = results.node['demand'].drop(reservoir_names, axis=1)
    demand_threshold=demands.sum().sum()*3600

    junctions_impacted[segment] = round(((demand_threshold/demand_at_inlet)*100),0)

    for index, row in dataframe.iterrows():
        if segment == row[2]:
            wn.remove_control('close pipe ' + index)
    wn.write_inpfile('networks/Inp_open_segment_'+'_'+fn+'.inp')

# Extract the number of junctions impacted by low pressure conditions for each pipe closure  
# number_of_junctions_impacted = dict([(k,v) for k,v in junctions_impacted.items()])

with open('criticality_valve_segments'+'_'+fn+'_'+'.pickle', 'wb') as handle:
    pickle.dump(junctions_impacted, handle, protocol=pickle.HIGHEST_PROTOCOL)
