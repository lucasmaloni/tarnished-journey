from node import Node
from edge import Edge
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.nodes = {}  # Dicionário de nós
        self.edges = {}  # Dicionário de arestas

    def add_node(self, node: Node):
        self.nodes[node.location] = node
        self.edges[node.location] = []  # Inicializa lista de adjacência para o nó

    def add_edge(self, start_node, end_node, distance, difficulty):
        if start_node in self.nodes and end_node in self.nodes:
            edge = Edge(start_node, end_node, distance, difficulty)
            self.edges[start_node].append(edge)
            edge_reverse = Edge(end_node, start_node, distance, difficulty)
            self.edges[end_node].append(edge_reverse)

    def get_neighbors(self, node_location):
        return self.edges.get(node_location, [])
    
    def display_graph(self):
        # Criando o grafo do NetworkX
        G = nx.Graph()

        # Adicionando nós e arestas ao NetworkX
        for node_location, node in self.nodes.items():
            # Garantir que as posições sejam floats
            x, y = float(node.position[0]), float(node.position[1])
            G.add_node(node_location, pos=(x, y))  # Adicionando posição com base em X, Y

        for node_location, neighbors in self.edges.items():
            for edge in neighbors:
                G.add_edge(node_location, edge.end_node, weight=edge.distance, difficulty=edge.difficulty)

        # Configurando as posições dos nós no gráfico
        pos = nx.get_node_attributes(G, 'pos')

        # Desenhando o grafo
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')

        # Desenhando os rótulos das arestas com base nos pesos (distância ou dificuldade)
        edge_labels = nx.get_edge_attributes(G, 'weight')  # Exibe as distâncias nas arestas
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        # Mostrar o gráfico
        plt.title('Visualização do Grafo de Localizações')
        plt.show()
