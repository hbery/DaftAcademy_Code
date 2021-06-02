def search_min_path(graph: dict, initial: str='START', destination: str='END') -> list:
    path = {}
    adj_node = {}
    queue = []
    result = []
    for node in graph:
        path[node] = float("inf")
        adj_node[node] = None
        queue.append(node)
        
    path[initial] = 0
    while queue:
        # find min distance which wasn't marked as current
        key_min = queue[0]
        min_val = path[key_min]
        for n in range(1, len(queue)):
            if path[queue[n]] < min_val:
                key_min = queue[n]  
                min_val = path[key_min]
        cur = key_min
        queue.remove(cur)
        for i in graph[cur]:
            alternate = graph[cur][i] + path[cur]
            if path[i] > alternate:
                path[i] = alternate
                adj_node[i] = cur
                
    result.append(destination)
    while True:
        destination = adj_node[destination]
        if destination is None:
            break
        result.append(destination)
    
    return result[::-1]


if __name__ == "__main__":
    graph = {
        'START': {'2_1': 2, '2_2': 5}, 
        '2_1': {'2_2': 5, '3_1': 4, '3_2': 8}, 
        '2_2': {'2_1': 2, '3_2': 8, '3_3': 2}, 
        '3_1': {'3_2': 8, 'END': 7}, 
        '3_2': {'3_1': 4, '3_3': 2, 'END': 7},
        '3_3': {'3_2': 8, 'END': 7},
        'END': {}
    }

    print(search_min_path(graph))