import time
from config import Neo4jConnection
import neo4j

class MovieSearch:
    def __init__(self, connection: Neo4jConnection):
        self.connection = connection

    def create_fulltext_index(self):
        query = """
        CREATE FULLTEXT INDEX Movie_plot_ft IF NOT EXISTS
        FOR (x:Movie)
        ON EACH [x.plot]
        """
        try:
            self.connection.execute_write(query)
            print("Full-text index created or already exists.")
        except neo4j.exceptions.Forbidden as e:
            print(f"Permission denied while creating full-text index: {e}")
            print("Proceeding without creating the index. Ensure it exists or ask an admin to create it.")


    def search_plot_murder_not_drugs_basic(self):
        query = """
        MATCH (m:Movie)
        WHERE m.plot CONTAINS 'murder' AND NOT m.plot CONTAINS 'drugs'
        RETURN m.title AS title, m.plot AS plot
        """
        return self.connection.execute_read(query)

    def search_plot_murder_and_drugs_fulltext(self):
        query = """
        CALL db.index.fulltext.queryNodes("Movie_plot_ft", "murder AND drugs")
        YIELD node
        RETURN node.title AS title, node.plot AS plot
        """
        return self.connection.execute_read(query)