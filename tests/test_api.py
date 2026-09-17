import os
import tempfile
import unittest

from app import create_app


class GeoMineApiTestCase(unittest.TestCase):
    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_file.close()
        class TestConfig:
            TESTING = True
            DATABASE = self.db_file.name
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def tearDown(self):
        os.unlink(self.db_file.name)

    def payload(self):
        return {"latitude": 23.5, "longitude": 87.2, "geology": 0.9, "geophysics": 0.8, "remote_sensing": 0.7}

    def test_health(self):
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_create_prediction_returns_201_and_inference(self):
        response = self.client.post("/api/v1/predictions", json=self.payload())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["data"]["classification"], "high")
        self.assertAlmostEqual(response.json["data"]["probability"], 0.825)

    def test_list_and_get_prediction(self):
        created = self.client.post("/api/v1/predictions", json=self.payload()).json["data"]
        listing = self.client.get("/api/v1/predictions")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(listing.json["count"], 1)
        fetched = self.client.get(f"/api/v1/predictions/{created['id']}")
        self.assertEqual(fetched.status_code, 200)
        self.assertEqual(fetched.json["data"]["id"], created["id"])

    def test_validation_is_400(self):
        response = self.client.post("/api/v1/predictions", json={"latitude": 100})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"]["code"], "VALIDATION_ERROR")

    def test_missing_prediction_is_404(self):
        response = self.client.get("/api/v1/predictions/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"]["code"], "NOT_FOUND")


if __name__ == "__main__":
    unittest.main()
