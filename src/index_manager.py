from config import Neo4jConnection

class IndexManager:
    def __init__(self, connection: Neo4jConnection):
        self.connection = connection

    def create_index(self):
        query = """
        CREATE INDEX Movie_year_imdbRating IF NOT EXISTS 
        FOR (m:Movie) ON (m.year, m.imdbRating)
        """
        self.connection.execute_write(query)

    def show_indexes(self):
        query = "SHOW INDEXES"
        return self.connection.execute_read(query)