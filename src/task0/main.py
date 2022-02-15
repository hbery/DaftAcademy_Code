import os
from algorithm import search_min_path


def populate_labels(entry_triangle: dict) -> dict:
    labels = {}
    for layer, elements in entry_triangle.items():
        for idx, element in enumerate(elements):
            label = "{}_{}".format(layer, idx+1)
            labels[label] = element

    start = labels['1_1']
    del labels['1_1']
    labels['START'] = start
    labels['END'] = start

    return labels


def create_graph(labels: dict, size: int) -> dict:
    graph = {}
    for node, flow in labels.items():
        # special cases
        if node == 'START':
            graph[node] = {'2_1': labels['2_1'], '2_2': labels['2_2']}
        elif node == 'END':
            graph[node] = {}
        else:
            graph[node] = {}
            # standard cases
            layer, index = node.split('_')
            left_neighbor = int(index) - 1
            right_neighbor = int(index) + 1
            left_child = int(index)
            right_child = int(index) + 1

            lneigh_label = None if (left_neighbor < 1) \
                else "{}_{}".format(int(layer), left_neighbor)
            rneigh_label = None if (right_neighbor > int(layer)) \
                else "{}_{}".format(int(layer), right_neighbor)
            lchild_label = "END" if (int(layer) == size) \
                else "{}_{}".format(int(layer)+1, left_child)
            rchild_label = None if (lchild_label == "END") \
                else "{}_{}".format(int(layer)+1, right_child)
            surroundings = [lneigh_label, rneigh_label,
                            lchild_label, rchild_label]

            for element in surroundings:
                if element is not None:
                    graph[node][element] = labels[element]

    return graph


def remap_labels(path: list, labels: dict) -> str:
    remapped = []
    for node in path:
        if node != 'END':
            remapped.append(labels[node])
    return ''.join([str(x) for x in remapped])


def sum_path(path: str) -> int:
    sum = 0
    for char in path:
        sum += int(char)
    return sum


def main():
    script_dir = os.path.dirname(__file__)
    rel_path = "data/3-medium.txt"
    abs_path = os.path.join(script_dir, rel_path)

    triangle = {}
    with open(abs_path, "r") as f:
        file = f.read().splitlines()
        file = [line.replace(' ', '') for line in file]
        for idx, line in enumerate(file):
            triangle[idx + 1] = [int(x) for x in line]

    SIZE = len(triangle)

    labels = populate_labels(triangle)
    # print(labels)

    graph = create_graph(labels, SIZE)
    # pprint.pprint(graph)

    result = search_min_path(graph)
    # print(result)

    remapped_result = remap_labels(result, labels)
    print(f"Path: {remapped_result}")

    summed_path = sum_path(remapped_result)
    print(f"Sum: {summed_path}")


if __name__ == "__main__":
    main()
