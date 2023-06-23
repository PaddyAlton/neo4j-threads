# tools/gdb_conn.py
# make it easy to connect to Neo4J from a terminal

from src.services.config import get_settings
from src.services.graph import build_cs, graph_init


def get_connected():
    settings = get_settings()
    connection_string = build_cs(
        settings.dbuser,
        settings.dbpass,
        "localhost:7687",
        settings.dbname,
    )
    graph_init(connection_string)

