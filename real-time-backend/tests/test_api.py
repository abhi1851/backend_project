import sys
import unittest
from pathlib import Path
from unittest.mock import patch

API_DIR = Path(__file__).resolve().parents[1] / "api"
sys.path.insert(0, str(API_DIR))

try:
    import app as api_app
except ModuleNotFoundError as e:
    if e.name in {"flask", "cassandra"}:
        api_app = None
    else:
        raise


class FakeRow:
    def __init__(self, **values):
        self.values = values

    def _asdict(self):
        return self.values


class FakeDb:
    def __init__(self, connected=True):
        self.connected = connected

    def is_connected(self):
        return self.connected

    def query(self, cql, params=()):
        return [
            FakeRow(bucket_ts="2026-05-07", key="meantemp", count=3, avg_value=24.5)
        ]


class ApiTestCase(unittest.TestCase):
    @unittest.skipIf(api_app is None, "API dependencies are not installed")
    def test_health_ok(self):
        with patch.object(api_app, "db", FakeDb(connected=True)):
            response = api_app.app.test_client().get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "status": "ok",
            "dependencies": {"cassandra": "ok"},
        })

    @unittest.skipIf(api_app is None, "API dependencies are not installed")
    def test_health_degraded(self):
        with patch.object(api_app, "db", FakeDb(connected=False)):
            response = api_app.app.test_client().get("/health")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json(), {
            "status": "degraded",
            "dependencies": {"cassandra": "unavailable"},
        })

    @unittest.skipIf(api_app is None, "API dependencies are not installed")
    def test_daily_avg(self):
        with patch.object(api_app, "db", FakeDb()):
            response = api_app.app.test_client().get("/api/data/daily-avg")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [
            {
                "bucket_ts": "2026-05-07",
                "key": "meantemp",
                "count": 3,
                "avg_value": 24.5,
            }
        ])


if __name__ == "__main__":
    unittest.main()
