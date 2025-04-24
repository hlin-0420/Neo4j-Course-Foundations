from config import Neo4jConnection, load_neo4j_config
from query_runner import QueryRunner
from index_manager import IndexManager
import neo4j
import os
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
conn = Neo4jConnection(uri=uri, user=username, password=password)

# Index management with error handling for insufficient privileges
try:
    index_mgr = IndexManager(conn)
    index_mgr.create_index()
    indexes = index_mgr.show_indexes()
    print("Indexes:", indexes)
except neo4j.exceptions.Forbidden as e:
    print(f"Permission denied while creating index: {e}")
    print("Make sure your user has the necessary privileges to perform schema operations.")
    indexes = index_mgr.show_indexes()
    print("Existing Indexes:", indexes)

# Query execution
query_runner = QueryRunner(conn)
query = """
MATCH (m:Movie)
WHERE 1990 <= m.year < 2000 AND m.imdbRating >= 8
RETURN m.title AS title, m.year AS year, m.imdbRating AS imdbRating
"""
records, profile = query_runner.profile_query(query)
print("Records:", records)
print("Profile Info:", profile)

# Close connection
conn.close()