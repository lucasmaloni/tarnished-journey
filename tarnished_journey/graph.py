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

    def display_graph(self, data_frame):
        # Criando o grafo do NetworkX
        G = nx.Graph()

        # Adicionando nós e arestas ao NetworkX
        for node_location, node in self.nodes.items():
            # Garantir que as posições sejam floats e inverter X e Y
            x, y = float(node.position[0]), float(node.position[1])
            G.add_node(node_location, pos=(y, -x))  # Adicionando posição com X como Y e Y como -X

        # Adicionar todos os nós, incluindo os que só aparecem como "Graça Chegada"
        for index, row in data_frame.iterrows():
            start_node = row['Graça Saída']
            end_node = row['Graça Chegada']

            # Garantir que o nó de chegada também seja adicionado ao grafo, caso não exista
            if end_node not in self.nodes:
                x, y = float(row['X - Chegada']), float(row['Y - Chegada'])
                self.nodes[end_node] = Node(end_node, x, y)  # Adicionando nó de "Graça Chegada"
                G.add_node(end_node, pos=(y, -x))  # Adicionando posição de "Graça Chegada" com X e Y invertidos

            # Agora, adicionamos as arestas, garantindo que sejam bilaterais
            distance = row['Tempo (s)']
            difficulty = row['Dificuldade']
            G.add_edge(start_node, end_node, weight=distance, difficulty=difficulty)
            G.add_edge(end_node, start_node, weight=distance, difficulty=difficulty)  # Aresta bilateral

        # Usando as posições X, Y passadas manualmente
        pos = nx.get_node_attributes(G, 'pos')

        # Verificando as posições manualmente antes de desenhar
        print("Posições dos Nós:", pos)

        # Desenhando o grafo com as posições fixadas
        plt.figure(figsize=(12, 10))  # Tamanho maior para melhor visualização
        nx.draw(G, pos, with_labels=True, node_size=300, node_color='Gold', font_size=10, font_weight='bold', edge_color='gray', 
                font_color='black', node_shape='o', width=1.5)

        # Garantir que os eixos X e Y tenham a mesma escala
        plt.axis('equal')  # Define a proporção igual para os eixos X e Y

        # Caso a origem seja no topo, inverte o eixo Y
        plt.gca().invert_yaxis()

        # Desenhando os rótulos das arestas com base nos pesos (distância ou dificuldade)
        edge_labels = nx.get_edge_attributes(G, 'weight')  # Exibe as distâncias nas arestas
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        # Mostrar o gráfico
        plt.title('Visualização do Grafo de Localizações')
        plt.show()