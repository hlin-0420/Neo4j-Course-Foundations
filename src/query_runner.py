from config import Neo4jConnection

class QueryRunner:
    def __init__(self, connection: Neo4jConnection):
        self.connection = connection

    def profile_query(self, query, parameters=None):
        profile_query = f"PROFILE {query}"
        with self.connection.driver.session() as session:
            result = session.run(profile_query, parameters)
            records = [record.data() for record in result]
            profile_info = result.consume().profile
            return records, profile_info

    def run_query(self, query, parameters=None):
        return self.connection.execute_read(query, parameters)