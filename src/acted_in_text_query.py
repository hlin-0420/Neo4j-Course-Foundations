from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt
import os
from config import Neo4jConnection, load_neo4j_config

# Get the directory two levels up from main.py (i.e., the project root)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Initialize connection

# Construct the full path to the movie-config.txt
config_path = os.path.join(project_root, "Encryption", "movie-config.txt")

# Load Configurations
config = load_neo4j_config(config_path)
uri = config.get("NEO4J_URI")
username = config.get("NEO4J_USERNAME")
password = config.get("NEO4J_PASSWORD")
driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to create TEXT index and query
def create_index_and_query(tx):
    # Comment out index creation if already done manually
    # tx.run("""
    # CREATE TEXT INDEX ACTED_IN_role_text IF NOT EXISTS 
    # FOR ()-[x:ACTED_IN]-() ON (x.role)
    # """)

    # Query with index hint
    result = tx.run("""
    PROFILE
    MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
    USING INDEX r:ACTED_IN(role)
    WHERE p.name CONTAINS 'George'
    AND r.role CONTAINS 'General'
    RETURN p.name AS person, r.role AS role, m.title AS movie
    """)
    
    return result.values()

# Query the database
with driver.session() as session:
    results = session.execute_write(create_index_and_query)

# Visualise results as a mind map
G = nx.Graph()

for person, role, movie in results:
    G.add_node(person, label='Person')
    G.add_node(movie, label='Movie')
    G.add_edge(person, movie, label=role)

# Draw the graph
pos = nx.spring_layout(G, seed=42)
labels = nx.get_edge_attributes(G, 'label')

plt.figure(figsize=(10, 8))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold', edge_color='gray')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red')

plt.title("Neo4j Movie Mind Map: 'George' as 'General'")
plt.show()

# Close the driver
driver.close()