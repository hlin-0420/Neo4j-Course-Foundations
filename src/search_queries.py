from config import Neo4jConnection

class MovieSearch:
    def __init__(self, connection: Neo4jConnection):
        self.connection = connection

    def search_title_night_sky(self):
        query = """
        MATCH (m:Movie)
        WHERE m.title CONTAINS 'Night' AND m.title CONTAINS 'Sky'
        RETURN m.title AS title
        """
        return self.connection.execute_read(query)

    def search_plot_murder_not_drugs(self):
        query = """
        MATCH (m:Movie)
        WHERE m.plot CONTAINS 'murder' AND NOT m.plot CONTAINS 'drugs'
        RETURN m.title AS title, m.plot AS plot
        """
        return self.connection.execute_read(query)

    def search_title_night_dead_plot_french(self):
        query = """
        MATCH (m:Movie)
        WHERE m.title CONTAINS 'Night' AND m.title CONTAINS 'Dead' AND m.plot CONTAINS 'French'
        RETURN m.title AS title, m.plot AS plot
        """
        return self.connection.execute_read(query)