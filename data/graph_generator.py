from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

root_data_dir = Path(__file__).parent


def generate_sequentially_connected_unweighted(nodes: int):
    data_dir = root_data_dir / "sequentially_connected_unweighted"
    data_dir.mkdir(parents=True, exist_ok=True)

    graph = nx.Graph([(node, node + 1) for node in range(1, nodes)])
    nx.draw(graph, with_labels=True)
    plt.savefig(data_dir / f"{nodes}.png")


def main():
    for nodes in range(2, 8):
        generate_sequentially_connected_unweighted(nodes)


if __name__ == "__main__":
    main()
