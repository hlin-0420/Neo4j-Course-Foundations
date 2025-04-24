from neo4j import GraphDatabase

def load_neo4j_config(filepath):
    config = {}
    with open(filepath, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key] = value
    return config

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
