import pandas as pd
from src.node import Node 
from src.graph import Graph

# Caminho do arquivo CSV
file_path = r'C:\Users\Lucas\Documents\Desenvolvimento\tarnished-journey\tarnished_journey\data\dados_elden_ring.csv'

# Carregar o arquivo CSV
data_frame = pd.read_csv(file_path, encoding='ISO-8859-1', sep=';', decimal = ',')

# Criando o grafo
graph = Graph()

# Passo 1: Garantir que TODOS os nós (de saída e chegada) sejam criados primeiro.
# Criamos um dicionário para guardar nós únicos e evitar duplicatas.
all_nodes_data = {}

# Lê nós da coluna de saída
for index, row in data_frame.iterrows():
    location, x, y = row['Graça Saída'], row['X - Saída'], row['Y - Saída']
    if location not in all_nodes_data:
        all_nodes_data[location] = (x, y)

# Lê nós da coluna de chegada
for index, row in data_frame.iterrows():
    location, x, y = row['Graça Chegada'], row['X - Chegada'], row['Y - Chegada']
    if location not in all_nodes_data:
        all_nodes_data[location] = (x, y)

# Adiciona todos os nós únicos ao grafo
for location, position in all_nodes_data.items():
    node = Node(location, position[0], position[1])
    graph.add_node(node)

# Passo 2: Agora que todos os nós existem, adicionamos as arestas com segurança.
for index, row in data_frame.iterrows():
    start_node = row['Graça Saída']
    end_node = row['Graça Chegada']
    distance = row['Tempo (s)']
    difficulty = row['Dificuldade']
    # Esta chamada agora funcionará para todas as arestas.
    graph.add_edge(start_node, end_node, distance, difficulty)

# Exibir a estrutura do grafo
graph.display_graph(data_frame)

start_node_name = "Ponte dos Santos"
end_node_name = "Cabana do Mercador"

print("\n--- Análise de Rota com Dijkstra ---")
print(f"Calculando a rota mais rápida de '{start_node_name}' para '{end_node_name}'...")

# Chama o algoritmo para encontrar o caminho
path, total_time = graph.dijkstra(start_node_name, end_node_name)

# Exibe o resultado no console
if path:
    print(f"\nRota encontrada! Tempo total: {total_time:.2f} segundos.")
    print("Caminho: " + " -> ".join(path))
    
    # Exibe o SEGUNDO grafo, agora com o caminho destacado
    print("\nExibindo o grafo com o caminho destacado...")
    graph.display_graph(data_frame, highlight_path=path)

else:
    print("\nNão foi possível encontrar uma rota entre os pontos especificados.")