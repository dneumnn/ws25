from kg_gen import KGGen

graph = KGGen.from_file("/Users/done/Documents/dneumnn/ws25/graph/graph.json")

KGGen.visualize(graph, output_path="./graph/graph.html", open_in_browser=True)