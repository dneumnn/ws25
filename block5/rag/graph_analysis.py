# Build a knowledge graph from scratch
# based on <https://medium.com/@lopezyse/knowledge-graphs-from-scratch-with-python-f3c2a05914cc>


import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from node2vec import Node2Vec
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import numpy as np

# Define the heads, relations, and tails
head = ['drugA', 'drugB', 'drugC', 'drugD', 'drugA', 'drugC', 'drugD', 'drugE', 'gene1', 'gene2','gene3', 'gene4', 'gene50', 'gene2', 'gene3', 'gene4']
relation = ['treats', 'treats', 'treats', 'treats', 'inhibits', 'inhibits', 'inhibits', 'inhibits', 'associated', 'associated', 'associated', 'associated', 'associated', 'interacts', 'interacts', 'interacts']
tail = ['fever', 'hepatitis', 'bleeding', 'pain', 'gene1', 'gene2', 'gene4', 'gene20', 'obesity', 'heart_attack', 'hepatitis', 'bleeding', 'cancer', 'gene1', 'gene20', 'gene50']


if __name__ == "__main__":
    # Create a dataframe
    df = pd.DataFrame({'head': head, 'relation': relation, 'tail': tail})
    #print(df)

    G = nx.Graph()
    #G2= nx.Graph()
    for (v1, e, v2) in zip(head, relation, tail):
        G.add_edge(v1, v2, label=e)
    #for _, row in df.iterrows():
    #    G2.add_edge(row['head'], row['tail'], label=row['relation'])

    print(G)
    #print(G2)

    
    # Visualize the knowledge graph
    pos = nx.spring_layout(G, seed=42, k=0.9)
    labels = nx.get_edge_attributes(G, 'label')
    
    print(nx.number_connected_components(G))

    for nodes in nx.connected_components(G):
        G_Sub = G.subgraph(nodes) 
        print(G_Sub)
    
    # Generate node embeddings using node2vec
    node2vec = Node2Vec(G, dimensions=64, walk_length=30, num_walks=200, workers=4) # You can adjust these parameters
    model = node2vec.fit(window=10, min_count=1, batch_words=4) # Training the model

    # Get embeddings for all nodes
    embeddings = np.array([model.wv[node] for node in G.nodes()])

    # Reduce dimensionality using t-SNE
    tsne = TSNE(n_components=2, perplexity=10)
    embeddings_2d = tsne.fit_transform(embeddings)
    """
    # Visualize embeddings in 2D space with node labels
    plt.figure(figsize=(12, 10))
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c='blue', alpha=0.7)

    # Add node labels
    for i, node in enumerate(G.nodes()):
        plt.text(embeddings_2d[i, 0], embeddings_2d[i, 1], node, fontsize=8)
    plt.title('Node Embeddings Visualization')
    plt.show()
    """
    # Perform K-Means clustering on node embeddings
    num_clusters = 3 # Adjust the number of clusters
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(embeddings)

    # Visualize clusters
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, font_size=10, node_size=700, node_color=cluster_labels, cmap=plt.cm.Set1, edge_color="gray", alpha=0.6)
    plt.title('Graph Clustering using K-Means')
    plt.show()


    """
    # Visualize K-Means clustering in the embedding space with node labels
    plt.figure(figsize=(12, 10))
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=cluster_labels, cmap=plt.cm.Set1, alpha=0.7)

    # Add node labels
    for i, node in enumerate(G.nodes()):
        plt.text(embeddings_2d[i, 0], embeddings_2d[i, 1], node, fontsize=8)
    
    plt.title('K-Means Clustering in Embedding Space with Node Labels')
    bar = plt.colorbar(label="Cluster Label")
    plt.show()
    """