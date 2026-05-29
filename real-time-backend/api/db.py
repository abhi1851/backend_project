from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel
import time

class CassandraClient:
    def __init__(self, host: str, keyspace: str):
        self.host = host
        self.keyspace = keyspace
        self.cluster = None
        self.session = None

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

    def connect(self, retries=30, delay=5):
        if self.session is None:
            self._connect_with_retry(retries=retries, delay=delay)

    def _setup_keyspace(self):
        self.session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
            WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }}
        """)
        self.session.set_keyspace(self.keyspace)

    def is_connected(self) -> bool:
        try:
            self.connect(retries=1, delay=0)
            self.session.execute("SELECT now() FROM system.local")
            return True
        except Exception as e:
            print(f"[Cassandra] health check failed: {e}")
            self.session = None
            self.cluster = None
            return False

    def query(self, cql: str, params: tuple = ()):
        self.connect()
        stmt = SimpleStatement(cql, consistency_level=ConsistencyLevel.ONE)
        return self.session.execute(stmt, params)
