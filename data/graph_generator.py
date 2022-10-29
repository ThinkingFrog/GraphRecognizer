from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import networkx as nx
from numpy.random import randint


def save_graph(graph_generator: Callable[[int], nx.Graph], nodes: int, dirname: str):
    root_data_dir = Path(__file__).parent

    data_dir = root_data_dir / dirname
    data_dir.mkdir(parents=True, exist_ok=True)

    filename = data_dir / f"{nodes}.png"
    filename.unlink(missing_ok=True)

    graph = graph_generator(nodes)

    pos = nx.drawing.nx_agraph.graphviz_layout(graph, prog="dot", args="-Grankdir=LR")
    nx.draw(
        graph,
        node_size=1000,
        arrowsize=50,
        with_labels=True,
        labels={n: n for n in graph.nodes},
        font_size=20,
        pos=pos,
    )
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels=nx.get_edge_attributes(graph, "weight")
    )

    plt.savefig(filename)
    plt.clf()


def generate_sequentially_connected_unweighted(nodes: int) -> nx.Graph:
    return nx.Graph([(node, node + 1) for node in range(1, nodes)])


def generate_fully_connected_unweighted(nodes: int) -> nx.Graph:
    return nx.Graph(
        [
            (node1, node2)
            for node1 in range(1, nodes + 1)
            for node2 in range(1, nodes + 1)
            if node1 != node2
        ]
    )


def generate_partially_connected_unweighted(nodes: int) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(1, nodes + 1))

    graph.add_edges_from(
        [
            (node1, node2)
            for node1 in graph.nodes
            for node2 in randint(1, nodes + 1, size=2)
            if node1 != node2
        ]
    )

    return graph


def generate_partially_unconnected_unweighted(nodes: int) -> nx.Graph:
    graph = generate_partially_connected_unweighted(int(nodes * 0.75))

    graph.add_nodes_from(range(int(nodes * 0.75), nodes + 1))

    return graph


def generate_partially_selfconnected_unweighted(nodes: int) -> nx.Graph:
    graph = generate_partially_connected_unweighted(nodes)

    graph.add_edges_from(
        [(node, node) for node in randint(1, nodes + 1, size=int(nodes * 0.25))]
    )

    return graph


def generate_unconnected_unweighted(nodes: int) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(1, nodes + 1))

    return graph


def make_weighted(generator: Callable[[int], nx.Graph], nodes: int) -> nx.Graph:
    graph = generator(nodes)

    for edge in graph.edges():
        graph[edge[0]][edge[1]]["weight"] = randint(1, 100)

    return graph


def make_negative_weighted(
    generator: Callable[[int], nx.Graph], nodes: int
) -> nx.Graph:
    graph = generator(nodes)

    for edge in graph.edges():
        graph[edge[0]][edge[1]]["weight"] = randint(-100, 0)

    return graph


def main():
    for nodes in range(2, 8):
        save_graph(
            generate_sequentially_connected_unweighted,
            nodes,
            "sequentially_connected_unweighted",
        )

        save_graph(
            lambda nodes: make_weighted(
                generate_sequentially_connected_unweighted, nodes
            ),
            nodes,
            "sequentially_connected_weighted",
        )

        save_graph(
            lambda nodes: make_negative_weighted(
                generate_sequentially_connected_unweighted, nodes
            ),
            nodes,
            "sequentially_connected_negative_weighted",
        )

    for nodes in range(2, 8):
        save_graph(
            generate_fully_connected_unweighted,
            nodes,
            "fully_connected_unweighted",
        )

        save_graph(
            lambda nodes: make_weighted(generate_fully_connected_unweighted, nodes),
            nodes,
            "fully_connected_weighted",
        )

        save_graph(
            lambda nodes: make_negative_weighted(
                generate_fully_connected_unweighted, nodes
            ),
            nodes,
            "fully_connected_negative_weighted",
        )

    for nodes in range(4, 11):
        save_graph(
            generate_partially_connected_unweighted,
            nodes,
            "partially_connected_unweighted",
        )

        save_graph(
            lambda nodes: make_weighted(generate_partially_connected_unweighted, nodes),
            nodes,
            "partially_connected_weighted",
        )

        save_graph(
            lambda nodes: make_negative_weighted(
                generate_partially_connected_unweighted, nodes
            ),
            nodes,
            "partially_connected_negative_weighted",
        )

    for nodes in range(4, 11):
        save_graph(
            generate_partially_unconnected_unweighted,
            nodes,
            "partially_unconnected_unweighted",
        )

        save_graph(
            lambda nodes: make_weighted(
                generate_partially_unconnected_unweighted, nodes
            ),
            nodes,
            "partially_unconnected_weighted",
        )

    for nodes in range(4, 11):
        save_graph(
            generate_partially_selfconnected_unweighted,
            nodes,
            "partially_selfconnected_unweighted",
        )

        save_graph(
            lambda nodes: make_weighted(
                generate_partially_selfconnected_unweighted, nodes
            ),
            nodes,
            "partially_selfconnected_weighted",
        )

    for nodes in range(2, 6):
        save_graph(
            generate_unconnected_unweighted,
            nodes,
            "unconnected_unweighted",
        )


if __name__ == "__main__":
    main()
