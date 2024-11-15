import unittest
from gps_module import data_gps


class TestGPSIntegration(unittest.TestCase):

    def test_gga_data_integration(self):
        gps_data_gga = "$GPGGA,123519.487,3754.587,N,14507.036,W,1,08,0.9,545.4,M,46.9,M,,*47"
        expected_output = {
            "latitude": 37.90978333333333,
            "longitude": -145.11726666666667,
            "altitude": 545.4,
            "speed": None,
            # Значение времени не проверяется в тесте
        }
        output = data_gps(gps_data_gga)

        # Выполнение тестирования
        self.assertAlmostEqual(output["latitude"], expected_output["latitude"], places=7)
        self.assertAlmostEqual(output["longitude"], expected_output["longitude"], places=7)
        self.assertEqual(output["altitude"], expected_output["altitude"])
        self.assertIsNone(output["speed"])

    def test_rmc_data_integration(self):
        gps_data_rmc = "$GPRMC,123519.487,A,3754.587,N,14507.036,W,000.0,360.0,120419,,,D"
        expected_output = {
            "latitude": 37.90978333333333,
            "longitude": -145.11726666666667,
            "altitude": None,
            "speed": 0.0,
            # Значение времени не проверяется в тесте
        }
        output = data_gps(gps_data_rmc)

        # Выполнение тестирования
        self.assertAlmostEqual(output["latitude"], expected_output["latitude"], places=7)
        self.assertAlmostEqual(output["longitude"], expected_output["longitude"], places=7)
        self.assertIsNone(output["altitude"])
        self.assertEqual(output["speed"], expected_output["speed"])


if __name__ == "__main__":
    unittest.main()
