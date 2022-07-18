import streamlit as st
import pandas as pd
import numpy as np
import time
import networkx as nx
import matplotlib.pyplot as plt

# Define function to trim edges based on weight; modified from source:
# Maksim Tsvetovat & Alexander Kouznetsov, Social Network Analysis for Startups, 2011
def trim_edges(g, weight, add_all_nodes):
    g2 = nx.Graph()
    for f, to, edata in g.edges(data=True):
        if edata['weight'] > weight or add_all_nodes == True:
            if f not in g2.nodes:
                g2.add_node(f, bipartite=g.nodes(data=True)[f]['bipartite'])
            if to not in g2.nodes:
                g2.add_node(to, bipartite=g.nodes(data=True)[to]['bipartite'])
        if edata['weight'] > weight:
            g2.add_edge(f, to, weight=edata['weight'])
    return g2

def drawGraph(wt=-1, iteration=-1):
    
    # Init globals
    global pos
    
    # Get threshold weight
    if wt == -1:
        sl1_state = st.session_state.sl1_key
        wt = sl1_state[0]
    wt = int(wt)
    
    # Get iteration number
    if iteration == -1:
        iteration = st.session_state.sb1_key
    iteration = int(iteration) - 1
    
    # Get a copy of the untrimmed graph
    gp = gp_init[iteration].copy()
    
    # Set plot dimensions
    fig = plt.gcf()
    fig.set_size_inches(figw, figh)
    fig.set_dpi(figdpi)
    fig.clf()

    # Trim the projected graph to the specified weight
    trimmed_gp = trim_edges(gp, wt, False)

    # Generate label dict
    labels = {}
    for node in gp.nodes():
        labels[node] = node

    # Draw graph
    if pos is None:
        pos = nx.random_layout(gp, seed=777)
    try:
        nx.draw_networkx_labels(trimmed_gp, pos=pos, labels=labels, font_size=14, font_color='black')
        nx.draw(trimmed_gp, pos=pos, nodelist=gp.nodes(), **options)
        nx.draw_networkx_nodes(trimmed_gp, pos=pos, **node_options)
    except:
        #ax = plt.gca()
        #ax.axis('off')
        #st.write(labels)
        pass
    plt.margins(x=0.4)
    plt.title('Round #' + str(iteration + 1) + ', Weight > ' + str(wt))
    pp.pyplot(plt, clear_figure=False)

def animateGraph():
    
    # Init globals
    global maxwt
    
    # Get weight start, stop, and step
    wt1 = sl1[0]
    wt2 = sl1[1]
    step = int(sl2)
    
    # Iterate through steps
    for i in range(wt1, wt2, step):
        drawGraph(i)
        time.sleep(.025)

# Set graph options
options = {
    'node_color': 'teal',
    'node_size': 200,
    'width': .75,
    'alpha': 0.4
}
node_options = {
    'node_color': 'teal',
    'node_size': 200,
    'alpha': 0.4,
    'linewidths': 0
}

# Set figure size
#plt.rcParams["figure.figsize"] = (4, 3)
figw = 12
figh = 8
figdpi = 5
fig = plt.figure(1, figsize=(figw, figh), dpi=figdpi)
#fig = plt.figure(1)
pp = st.pyplot(fig)

# Load graph data
gp_init = []
maxwt = 0
for i in range(0, 3):
    
    # Load data from gml file
    g = nx.read_gml('gp' + str(i + 1) + '.gml')
    gp_init.append(g)
    
    # Find the maximum edge weight to use as the slider range
    wt = max([e[2]['weight'] for e in gp_init[i].edges(data=True)])
    if wt > maxwt: maxwt = wt

# Create controls
sb1 = st.sidebar.selectbox('Round #', (1, 2, 3), 0, key='sb1_key', on_change=drawGraph)
sl1 = st.sidebar.slider('Weight', 0, maxwt, (0, maxwt), key='sl1_key', on_change=drawGraph)
sl2 = st.sidebar.slider('Step', 1, 100, 5, on_change=drawGraph)
but1 = st.sidebar.button('Animate', on_click=animateGraph)

# Draw initial graph
pos = None
drawGraph(int(sl1[0]))
