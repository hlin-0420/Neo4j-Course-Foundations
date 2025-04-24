import time
import pandas as pd
import os
from config import Neo4jConnection, load_neo4j_config
from search_queries import MovieSearch

# Ensure output directory exists
output_dir = os.path.join(os.path.dirname(__file__), "..", "Output")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "plot_search_comparison.csv")

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

# Ensure Full-Text Index exists
import neo4j

# Ensure Full-Text Index exists
try:
    search.create_fulltext_index()
except neo4j.exceptions.Forbidden as e:
    print(f"Permission denied while creating full-text index: {e}")
    print("Proceeding without creating index. Ensure it exists or contact admin.")

# Time basic CONTAINS search
start_basic = time.time()
basic_results = search.search_plot_murder_not_drugs_basic()
end_basic = time.time()
basic_duration = end_basic - start_basic

# Time Full-Text search
start_ft = time.time()
ft_results = search.search_plot_murder_and_drugs_fulltext()
end_ft = time.time()
ft_duration = end_ft - start_ft

# Print Results Summary
print(f"Basic Search Time: {basic_duration:.4f} seconds, Results: {len(basic_results)}")
print(f"Full-Text Search Time: {ft_duration:.4f} seconds, Results: {len(ft_results)}")

# Save to CSV for comparison
comparison_data = {
    "Method": ["Basic CONTAINS", "Full-Text Search"],
    "Execution Time (s)": [basic_duration, ft_duration],
    "Results Count": [len(basic_results), len(ft_results)]
}

df = pd.DataFrame(comparison_data)
df.to_csv(output_file, index=False)
print(f"Comparison saved to {output_file}")

# Close connection
conn.close()