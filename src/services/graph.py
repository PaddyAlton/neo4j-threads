# services/graph.py
# services for interacting with the graph database

from time import sleep, time

from neo4j.io import ServiceUnavailable
from neomodel import config, db


def build_cs(dbuser: str, dbpass: str, dbhost: str, dbname: str) -> str:
    """
    build_cs

    Returns a connection string built from the inputs

    Inputs:
        dbuser - username
        dbpass - user password
        dbhost - host + port (e.g. localhost:7687)
        dbname - name of the database

    Output:
        connection_string

    """
    return f"bolt://{dbuser}:{dbpass}@{dbhost}/{dbname}"


def graph_init(connection_string: str):
    """
    graph_init

    Specify the connection to the graph database, await its availability

    Inputs:
        connection_string (e.g. bolt://user:password@host:port/dbname)

    """
    config.DATABASE_URL = connection_string

    timeout = 10.0  # seconds
    start_time = time()

    while time() - start_time < timeout:
        try:
            db.cypher_query("RETURN 1")  # succeeds IFF database is available
            return
        except ServiceUnavailable:
            sleep(3)

    missing_host = connection_string.split("@")[-1]

    raise ServiceUnavailable(f"Neo4J database not found at {missing_host}")
