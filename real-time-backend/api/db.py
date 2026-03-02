from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from  cassandra import ConsistencyLevel
import time

class CassandraClient:
    def __init__(self, host: str, keyspace: str):
        self.host = host
        self.keyspace = keyspace
        self._connect_with_retry()

    def _connect_with_retry(self, retries=30, delay=5):
        for i in range(retries):
            try:
                self.cluster = Cluster([self.host])
                self.session = self.cluster.connect()
                self._setup_keyspace()
                return
            except Exception as e:
                print(f"[Cassandra] connect attempt {i+1}/{retries} failed: {e}")
                time.sleep(delay)
        raise RuntimeError("Unable to connect to Cassandra")

    def _setup_keyspace(self):
        self.session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
            WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }}
        """)
        self.session.set_keyspace(self.keyspace)

    def query(self, cql: str, params: tuple = ()):
        stmt = SimpleStatement(cql, consistency_level=ConsistencyLevel.ONE)
        return self.session.execute(stmt, params)