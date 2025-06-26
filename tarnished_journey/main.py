import pandas as pd
from node import Node  # Supondo que a classe Node esteja no arquivo node.py
from edge import Edge  # Supondo que a classe Edge esteja no arquivo edge.py
from graph import Graph  # Supondo que a classe Graph esteja no arquivo graph.py

# Caminho do arquivo CSV
file_path = r'C:\Users\lucas\OneDrive\Documentos\Desenvolvimento\tarnished-journey\tarnished-journey\tarnished_journey\data\dados_elden_ring.csv'

# Carregar o arquivo CSV
df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=';', decimal = ',')

# Criando o grafo
graph = Graph()

# Adicionando os nós ao grafo
nodes = {}

for index, row in df.iterrows():
    # Criando o nó com a localização e coordenadas
    node = Node(row['Graça Saída'], row['X - Saída'], row['Y - Saída'])
    nodes[row['Graça Saída']] = node
    graph.add_node(node)

# Adicionando as arestas entre os nós
for index, row in df.iterrows():
    start_node = row['Graça Saída']
    end_node = row['Graça Chegada']
    distance = row['Tempo (s)']  # Tempo de viagem (distância)
    difficulty = row['Dificuldade']  # Dificuldade do caminho
    
    graph.add_edge(start_node, end_node, distance, difficulty)

# Exibir a estrutura do grafo
graph.display_graph()
