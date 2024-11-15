import unittest
from gps_module import data_gps


class TestGPSSystem(unittest.TestCase):

    def test_valid_gga_data(self):
        gps_data_gga = "$GPGGA,123456.78,4916.45,N,12311.12,W,1,12,0.5,30.0,M,0.0,M,,*47"
        expected_output = {
            "latitude": 49 + (16.45 / 60),  # 49.27425
            "longitude": -(123 + (11.12 / 60)),  # -123.18533333333334
            "altitude": 30.0,
            "speed": None,
        }
        output = data_gps(gps_data_gga)

        # Выполнение тестирования
        self.assertAlmostEqual(output["latitude"], expected_output["latitude"], places=7)
        self.assertAlmostEqual(output["longitude"], expected_output["longitude"], places=7)
        self.assertEqual(output["altitude"], expected_output["altitude"])
        self.assertIsNone(output["speed"])

    def test_valid_rmc_data(self):
        gps_data_rmc = "$GPRMC,123519.487,A,3754.587,N,14507.036,W,000.0,360.0,120419,,,D"
        expected_output = {
            "latitude": 37 + (54.587 / 60),  # 37.90978333333333
            "longitude": -(145 + (7.036 / 60)),  # -145.11726666666667
            "altitude": None,
            "speed": 0.0,
        }
        output = data_gps(gps_data_rmc)

        # Выполнение тестирования
        self.assertAlmostEqual(output["latitude"], expected_output["latitude"], places=7)
        self.assertAlmostEqual(output["longitude"], expected_output["longitude"], places=7)
        self.assertIsNone(output["altitude"])
        self.assertEqual(output["speed"], expected_output["speed"])

    def test_invalid_data(self):
        gps_data_invalid = "$GPGGA,12345,,N,,W,1,08,0.9,,,M,46.9,M,,47"
        output = data_gps(gps_data_invalid)
        self.assertIsNone(output)  # Ожидается, что выход будет None

    def test_edge_case(self):
        gps_data_edge_case = "$GPRMC,000000.000,V,0000.0000,N,00000.0000,W,000.0,000.0,010101,,,D"
        output = data_gps(gps_data_edge_case)
        self.assertIsNotNone(output)  # Ожидается, что выход не будет None

        self.assertEqual(output["latitude"], 0.0)  # Ожидается, что широта будет 0
        self.assertEqual(output["longitude"], 0.0)  # Ожидается, что долгота будет 0


if __name__ == "__main__":
    unittest.main()
