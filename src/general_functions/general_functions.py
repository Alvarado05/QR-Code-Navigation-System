import math
import numpy as np
def stepsToCardinality(steps, nodes):
    """
    Converts steps of nodes to cardinality directions based on the robot's map
    inputs:
        steps: list of nodes the robot needs to pass through to get to its destination
        nodes: dataframe of nodes in map
    output:
        cardinality: list of cardinality of each node from last node
    """
    start_step = steps[0]
    cardinality = []
    last_step = start_step
    for step in steps:
        if step  == start_step:
            cardinality.append(0)
        else:
            sub = nodes.loc[step] - nodes.loc[last_step]

            if sub['X'] == 0:
                num = sub['Y']
                if num > 0: 
                    cardinality.append('N')
                else:
                    cardinality.append('S')
            elif sub['Y'] == 0:
                num = sub['X']
                if num > 0:
                    cardinality.append('E')
                else:
                    cardinality.append('W')

            else:
                print("It moves in bothe x and y")
        last_step = step
    return cardinality

def cardToOrientation(cardinalitites, direcDict):
    """
    Returns a list of the angles for each cardinal point.

    Accepts as inputs:

    cardinalitites: A list with the cardinal points of the path.
    
    direcDict: Dictionary that contains the cardinal points as key and the angles of each cardinal points as the values.
    """
    converted = []
    for i in cardinalitites:
        for j in direcDict:
            if i == j:
                converted.append(direcDict[j])
    return converted

def northToCardinal(north):
    # recibe el norte en radianes y la tolerancia del angulo mas pequeno y mas grande
    # debe regresar un diccionario con los puntos cardinales calculados con respecto a ese norte
    Dict = {'N':round(north, 3), 'E': round(north + 3*(math.pi/2), 3), 'S': round(north + math.pi, 3), 'W': round(north + (math.pi/2), 3)}

    for i in Dict.keys():
        if Dict[i] > math.pi*2:
            Dict[i] = round(Dict[i] - math.pi*2, 3)
            
    return Dict