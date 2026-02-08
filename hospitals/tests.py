from django.test import TestCase

from .utils import haversine


class HaversineTest(TestCase):
    def test_same_point(self):
        self.assertAlmostEqual(haversine(48.8566, 2.3522, 48.8566, 2.3522), 0.0)

    def test_paris_to_lyon(self):
        # Paris → Lyon ~ 392 km
        dist = haversine(48.8566, 2.3522, 45.7640, 4.8357)
        self.assertAlmostEqual(dist, 392, delta=10)

    def test_short_distance(self):
        # Pitié-Salpêtrière → Hôtel-Dieu ~ 1.9 km
        dist = haversine(48.8380, 2.3655, 48.8534, 2.3488)
        self.assertAlmostEqual(dist, 1.9, delta=0.5)

    def test_symmetry(self):
        d1 = haversine(48.8566, 2.3522, 45.7640, 4.8357)
        d2 = haversine(45.7640, 4.8357, 48.8566, 2.3522)
        self.assertAlmostEqual(d1, d2, places=6)


class NearestAPITest(TestCase):
    def test_missing_params(self):
        resp = self.client.get('/api/nearest/')
        self.assertEqual(resp.status_code, 400)

    def test_invalid_params(self):
        resp = self.client.get('/api/nearest/?lat=abc&lon=def')
        self.assertEqual(resp.status_code, 400)
