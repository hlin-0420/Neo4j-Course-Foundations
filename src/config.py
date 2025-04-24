from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver:
            self.driver.close()

    def execute_read(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.execute_read(lambda tx: tx.run(query, parameters).data())
            return result

    def execute_write(self, query, parameters=None):
        with self.driver.session() as session:
            session.execute_write(lambda tx: tx.run(query, parameters))
