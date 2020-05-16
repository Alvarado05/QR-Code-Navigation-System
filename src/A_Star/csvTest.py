import pandas as pd
import aStar
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

FILE_NODE = None
FILE_CONNECTION = None
CONNECTIONS = None
NODES = None

def loadCSVFiles():
    global FILE_NODE
    global FILE_CONNECTION
    global CONNECTIONS
    global NODES

    FILE_NODE = "src/A_Star/Maps/SecondFloorG.csv"
    FILE_CONNECTION = "src/A_Star/Maps/SecondFloorConnections.csv"
    CONNECTIONS = pd.read_csv(FILE_CONNECTION)
    NODES = pd.read_csv(FILE_NODE, index_col = 'Nodes')

def createNodes(nodes, grafo):
    nodeNames = nodes.index
    for i in range(len(nodeNames)):
        coor = nodes.iloc[i,:].values.tolist()
        grafo.add_node(nodeNames[i], pos=(coor[0], coor[1]))

def createConnections(connections, grafo):
    connections = connections[0]
    for i in range(connections.index.size):
        conNodes = connections.iloc[i,:].values.tolist()
        grafo.add_edge(conNodes[0], conNodes[1])

def drawGraph(self):
    global CONNECTIONS
    global NODES
    loadCSVFiles()
    createMap(NODES, CONNECTIONS)

def createMap(nodes, *connections):
    grafo = nx.Graph()
    fig, ax = plt.subplots()

    createNodes(nodes, grafo)    

    if not connections:
        print(type(connections))
    else:
        createConnections(connections, grafo)

    pos = nx.get_node_attributes(grafo, 'pos')
    nx.draw(grafo, pos, with_labels=True)
    
    limits = plt.axis('on')
    aref = plt.axes([0.7, 0.05, 0.1, 0.075])
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

    refresh = Button(aref, 'Refresh')
    refresh.on_clicked(drawGraph)

    plt.show()

loadCSVFiles()
createMap(NODES, CONNECTIONS)



