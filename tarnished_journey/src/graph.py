from src.node import Node
from src.edge import Edge
import networkx as nx
import matplotlib.pyplot as plt
import heapq

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

    def display_graph(self, data_frame, highlight_path=None): # Parâmetro novo
        G = nx.Graph()

        # Lógica original para adicionar nós e posições
        for node_location, node in self.nodes.items():
            x, y = float(node.position[0]), float(node.position[1])
            G.add_node(node_location, pos=(y, -x))

        # Lógica original para garantir que todos os nós de chegada existam
        for index, row in data_frame.iterrows():
            start_node = row['Graça Saída']
            end_node = row['Graça Chegada']
            if end_node not in self.nodes:
                x, y = float(row['X - Chegada']), float(row['Y - Chegada'])
                self.nodes[end_node] = Node(end_node, x, y)
                G.add_node(end_node, pos=(y, -x))
            
            distance = row['Tempo (s)']
            difficulty = row['Dificuldade']
            G.add_edge(start_node, end_node, weight=distance, difficulty=difficulty)

        pos = nx.get_node_attributes(G, 'pos')
        
        # Desenho original do grafo
        plt.figure(figsize=(16, 12))
        nx.draw(G, pos, with_labels=True, node_size=300, node_color='Gold', font_size=9, edge_color='gray')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

        # Se um caminho para destacar foi fornecido, desenhe-o por cima.
        if highlight_path and len(highlight_path) > 1:
            path_edges = list(zip(highlight_path, highlight_path[1:]))
            nx.draw_networkx_nodes(G, pos, nodelist=highlight_path, node_color='red', node_size=400)
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2.5)

        plt.title('Visualização do Grafo de Localizações')
        plt.axis('equal')
        plt.gca().invert_yaxis()
        plt.show()
    
    def dijkstra(self, start_location, end_location):
        distances = {node: float('inf') for node in self.nodes}
        # Verificação para garantir que o nó de partida existe antes de acessá-lo
        if start_location not in distances:
            return None, float('inf') # Retorna se o nó de partida não for válido
        
        distances[start_location] = 0
        
        previous_nodes = {node: None for node in self.nodes}
        priority_queue = [(0, start_location)]

        path_found = False
        while priority_queue:
            current_distance, current_location = heapq.heappop(priority_queue)

            if current_distance > distances[current_location]:
                continue
            if current_location == end_location:
                path_found = True
                break

            for edge in self.get_neighbors(current_location):
                neighbor_location = edge.end_node
                # Se o vizinho por acaso não estiver no dict de distâncias, pule-o.
                if neighbor_location not in distances:
                    continue
                    
                weight = edge.distance
                distance_through_current = distances[current_location] + weight

                if distance_through_current < distances[neighbor_location]:
                    distances[neighbor_location] = distance_through_current
                    previous_nodes[neighbor_location] = current_location
                    heapq.heappush(priority_queue, (distance_through_current, neighbor_location))
        
        # Se o caminho não foi encontrado ou o nó de destino é inalcançável
        if not path_found or distances[end_location] == float('inf'):
            return None, float('inf')

        path = []
        current_node = end_location
        while current_node is not None:
            path.insert(0, current_node)
            current_node = previous_nodes[current_node]
            
        return path, distances[end_location]