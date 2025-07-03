import pandas as pd
from src.node import Node 
from src.graph import Graph
from pathlib import Path


script_dir = Path(__file__).parent
file_path = script_dir / "data" / "dados_elden_ring.csv"
data_frame = pd.read_csv(file_path, encoding='ISO-8859-1', sep=';', decimal = ',')

graph = Graph()

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

# que todos os nós existem, adicionamos as arestas com segurança.
for index, row in data_frame.iterrows():
    start_node = row['Graça Saída']
    end_node = row['Graça Chegada']
    distance = row['Tempo (s)']
    difficulty = row['Dificuldade']
    
    graph.add_edge(start_node, end_node, distance, difficulty)
            
while True:
    
    print("Digite o que deseja fazer:")
    print("1- Plotar o grafo")
    print("2- Mostrar o grafo com rota calculada pelo Dijkstra")
    print("3- Fazer uma BFS a partir de um Nó")
    print("4- Análise de hub central")
    print("5- Análise de centralidade de intermediação")
    print("6- Análise de Centralidade de Proximidade")
    print("0- Sair\n")
    choice = int(input("Entrada: "))
    
    if choice == 1:
        #Plotagem Grafo criado
        graph.display_graph(data_frame)
        
    elif choice == 2:
        start_node_name = "Quarta Igreja de Marika" #Nó saída
        end_node_name = "Túnel ao Castelo" #Nó chegada

        path, total_time = graph.dijkstra(start_node_name, end_node_name)

        if path:
            graph.display_graph(data_frame, highlight_path=path)
        else:
            print("\nNão foi possível encontrar uma rota entre os pontos especificados.")
            
    elif choice == 3:
        #Demonstração BFS
        start_node = "Porão Arruinado"
        max_jumps = 3

        print(f"\n--- Análise de Proximidade (BFS) ---")
        print(f"Buscando locais a até {max_jumps} saltos de distância de '{start_node}':")

        nearby_locations = graph.bfs_by_level(start_node, max_jumps)
        
        if not nearby_locations:
            print("Nenhum local encontrado dentro do número de saltos especificado.")
        else:
            for level in sorted(nearby_locations.keys()):
                locations = sorted(nearby_locations[level])
                print(f"\nLocais a {level} salto(s) de distância:")
                for loc in locations:
                    print(f"  - {loc}")
    
    elif choice ==4:
        node, value = graph.calculate_degree_centrality()
        
        if node:
            graph.display_graph(data_frame, highlight_nodes=[node])
        else:
            print("Não foi possível calcular a centralidade.")
    
    elif choice == 5:
        node, value = graph.calculate_betweenness_centrality()
        
        if node:
            graph.display_graph(data_frame, highlight_nodes=[node])
            
        else:
            print("Não foi possível calcular a centralidade.")
    
    elif choice == 6:
        node, value = graph.calculate_closeness_centrality()
        
        if node:
            
            print("\nExibindo o mapa com o nó de melhor acesso destacado...")
            graph.display_graph(data_frame, highlight_nodes=[node])
            
        else:
            print("Não foi possível calcular a centralidade.")
    
    elif choice == 0:
        print("Flw!")
        break
    
    else:
        print("Entrada inválida irmãozinho! Preste atenção!!")