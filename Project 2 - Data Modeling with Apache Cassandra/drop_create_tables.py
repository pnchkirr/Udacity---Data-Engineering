from cassandra.cluster import Cluster
from cql_queries import drop_table_queries, create_table_queries


def drop_tables(session):
    """
    Drops each table using the queries in `drop_table_queries` list
    """
    
    for query in drop_table_queries:
        session.execute(query)
        
def create_tables(session):
    """
    Creates each table using the queries in `create_table_queries` list
    """
    
    num_queries = len(create_table_queries)
    
    for i, query in enumerate(create_table_queries, 1):
        session.execute(query)
        print('{}/{} tables created.'.format(i, num_queries))