from neo4j import GraphDatabase
import networkx as nx
from pyvis.network import Network
import os
from config import Neo4jConnection, load_neo4j_config
import webbrowser

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

# Visualise results using Pyvis
G = nx.Graph()

for person, role, movie in results:
    G.add_node(person, label='Person')
    G.add_node(movie, label='Movie')
    G.add_edge(person, movie, label=role)

# Convert NetworkX graph to Pyvis
net = Network(height='750px', width='100%', notebook=False, bgcolor='#222222', font_color='white')
net.from_nx(G)

# Customize nodes
for node in net.nodes:
    if node['label'] == 'Person':
        node['color'] = 'skyblue'
        node['size'] = 25
    else:
        node['color'] = 'lightgreen'
        node['size'] = 20

# Customize edges
for edge in net.edges:
    edge['title'] = edge['label']
    edge['color'] = 'red'

# Save and show the result
output_path = os.path.join(project_root, "neo4j_movie_mind_map.html")
net.write_html(output_path)
webbrowser.open("file://" + output_path)

# Close the driver
driver.close()