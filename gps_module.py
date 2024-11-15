import time


def convert_to_decimal(degree_str, direction):
    """Преобразует строку с градусами в десятичный формат."""
    # Преобразуем строку в float
    degree_value = float(degree_str)
    degrees = int(degree_value // 100)
    minutes = degree_value % 100
    decimal = degrees + (minutes / 60.0)
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal


def get_timestamp(timestamp_str):
    # Форматирование даты для mktime
    # Текущая дата, чтобы использовать её вместе со временем
    current_time = time.localtime()
    current_date = time.strftime("%Y,%m,%d", current_time).split(',')
    year, month, day = int(current_date[0]), int(current_date[1]), int(current_date[2])

    # Преобразование времени
    timestamp = time.strptime(f"{timestamp_str},{year},{month},{day}", "%H%M%S.%f,%Y,%m,%d")
    return time.mktime(timestamp)


def data_gps(gps_data):
    """Обработка данных с GPS.

    Args:
        gps_data: Строка данных в формате NMEA.

    Returns:
        Словарь с обработанными данными:
        - latitude: Широта (градусы).
        - longitude: Долгота (градусы).
        - altitude: Высота (метры).
        - speed: Скорость (м/с).
        - timestamp: Время (секунды).
    """

    nmea_formats = {
        # Описание структуры формата GGA
        "$GPGGA": {
            "timestamp": 1,
            "latitude": (2, 3),
            "longitude": (4, 5),
            "altitude": 9,
            "speed": None,  # Скорость не доступна в GGA
            "speed_multiplier": None
        },
        # Описание структуры формата RMC
        "$GPRMC": {
            "timestamp": 1,
            "latitude": (3, 4),
            "longitude": (5, 6),
            "altitude": None,  # Высота недоступна в RMC
            "speed": 7,
            "speed_multiplier": 0.514444  # Преобразование узлов в м/с
        }
    }

    try:
        # Разделение строки NMEA по запятым
        data_parts = gps_data.split(",")

        hdr = data_parts[0]
        if hdr not in nmea_formats:
            raise ValueError("Неизвестный формат NMEA")

        timestamp_str = data_parts[nmea_formats[hdr]["timestamp"]]
        latitude = convert_to_decimal(data_parts[nmea_formats[hdr]["latitude"][0]],
                                      data_parts[nmea_formats[hdr]["latitude"][1]])
        longitude = convert_to_decimal(data_parts[nmea_formats[hdr]["longitude"][0]],
                                       data_parts[nmea_formats[hdr]["longitude"][1]])
        altitude = None if nmea_formats[hdr]["altitude"] is None else float(data_parts[nmea_formats[hdr]["altitude"]])
        speed = None if nmea_formats[hdr]["speed"] is None else \
            float(data_parts[nmea_formats[hdr]["speed"]]) * float(nmea_formats[hdr]["speed_multiplier"])

        # Возвращение обработанных данных
        return {
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude,
            "speed": speed,
            "timestamp": get_timestamp(timestamp_str)
        }

    except Exception as e:
        print("Ошибка при обработке данных GPS:", e)
        return None


if __name__ == "__main__":
    # Реализация алгоритма
    gps_data_gga = "$GPGGA,123519.487,3754.587,N,14507.036,W,1,08,0.9,545.4,M,46.9,M,,*47"
    gps_data_rmc = "$GPRMC,123519.487,A,3754.587,N,14507.036,W,000.0,360.0,120419,,,D"

    data_gps_gga = data_gps(gps_data_gga)
    data_gps_rmc = data_gps(gps_data_rmc)

    for data_source, data_gps_obj in zip(["GGA", "RMC"], [data_gps_gga, data_gps_rmc]):
        if data_gps_obj:
            print(f"Обработанные данные из {data_source}:")
            print(f"Широта: {data_gps_obj['latitude']}")
            print(f"Долгота: {data_gps_obj['longitude']}")
            print(f"Высота: {data_gps_obj['altitude']}")
            print(f"Скорость: {data_gps_obj['speed']}")
            print(f"Время: {data_gps_obj['timestamp']}")
        else:
            print(f"Некорректные данные GPS из {data_source}.")
