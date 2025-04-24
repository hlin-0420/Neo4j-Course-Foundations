from config import Neo4jConnection, load_neo4j_config
from search_queries import MovieSearch
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
search = MovieSearch(conn)

# Search for titles containing 'Night' followed by 'Sky'
night_sky_results = search.search_title_night_sky()
print("Titles with 'Night' and 'Sky':", night_sky_results)

# Search for plots with 'murder' but not 'drugs'
murder_not_drugs_results = search.search_plot_murder_not_drugs()
print("Plots with 'murder' but not 'drugs':", murder_not_drugs_results)

# Search for titles with 'Night' and 'Dead' and plot with 'French'
night_dead_french_results = search.search_title_night_dead_plot_french()
print("Titles with 'Night' and 'Dead' and plot with 'French':", night_dead_french_results)

# Close connection
conn.close()