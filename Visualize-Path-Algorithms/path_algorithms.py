from collections import deque
from math import inf


def depth_first_search(current_node, end_node, visited):
    visited.append(current_node)
    if current_node == end_node:
        return
    for neighbor in current_node.neighbors:
        if neighbor not in visited:
            neighbor.backpointer = current_node
            depth_first_search(neighbor, end_node, visited)


def breadth_first_search(start_node, end_node, graph):
    
    visited = [start_node]
    que = deque()
    que.append(start_node)
    start_node.backpointer = None

    while not end_node in visited and len(que) > 0:
        popped = que.popleft()
        visited.append(popped)
        for neighbor in popped.neighbors:
            if neighbor not in visited:
                neighbor.backpointer = popped
                visited.append(neighbor)
                que.append(neighbor)


def dijstras_algorithm(start_node, end_node, graph):                
    graph.reset()
    
    start_node.distance = 0
    visited = []
    count = 1
    current_node = start_node
    while current_node is not end_node:
        
        
        current_node.order = count
        visited.append(current_node)
        for neighbor in current_node.neighbors:
            if neighbor not in visited and \
                    current_node.distance + current_node.get_cartesian_distance(neighbor) < neighbor.distance:
                neighbor.distance = current_node.get_cartesian_distance(neighbor) + current_node.distance
                neighbor.backpointer = current_node

        min_dis = inf
        min_node = None
        for node in graph.node_list:
            if node.distance < min_dis and node not in visited:
                min_dis = node.distance
                min_node = node
        current_node = min_node


def a_star_algorithm(start_node, end_node, graph):
    graph.reset()
    start_node.distance = 0
    visited = []
    count = 1
    current_node = start_node
    while current_node is not end_node:
        current_node.order = count
        visited.append(current_node)
        for neighbor in current_node.neighbors:
            if neighbor not in visited and \
                    current_node.distance + current_node.get_cartesian_distance(neighbor) < neighbor.distance:
                neighbor.distance = current_node.get_cartesian_distance(neighbor) + current_node.distance
                neighbor.backpointer = current_node

        min_dis = inf
        min_node = None
        for node in graph.node_list:
            if node.distance + node.get_cartesian_distance(end_node) < min_dis \
                    and node not in visited:
                min_dis = node.distance + node.get_cartesian_distance(end_node)
                min_node = node
        current_node = min_node
