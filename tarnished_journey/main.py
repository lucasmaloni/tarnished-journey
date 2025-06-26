import pandas as pd
from node import Node 
from graph import Graph

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
