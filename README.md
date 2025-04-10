# Neo4j Course Foundations
 The course materials for the foundations of Neo4j. 

Installation Steps

1. Create a virtual Environment for installing dependencies.

a. Install the virtual environment

```
python -m venv your_venv_name
```

b. Activate the virtual environment.

On Windows:
```
your_venv_name\Scripts\activate
```

On macOS/Linux
```
source your_venv_name/bin/activate
```

2. Install the Dependencies

```
pip install -r requirements.txt
```

3. Verify the installation.
After setting up the application, run the following Python code to verify if Neo4j connection is set-up.

```python
from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"  # Replace with your Neo4j instance URI
AUTH = ("neo4j", "your_password")  # Replace with your Neo4j username and password

driver = GraphDatabase.driver(URI, auth=AUTH)

with driver.session() as session:
    session.run("RETURN 'Connection successful!'")
    print("Connection established.")
```