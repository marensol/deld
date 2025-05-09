import logging
import threading
import time
import math
import requests

from messaging import SensorMeasurement
import common


class Sensor:

    def __init__(self, did):
        self.did = did
        self.measurement = SensorMeasurement(did=did, value='0.0')

    def simulator(self):
        logging.info(f"Sensor {self.did} starting")

        while True:
            temp = round(math.sin(time.time() / 10) * common.TEMP_RANGE, 1)
            logging.info(f"Sensor {self.did}: {temp}")
            self.measurement.set_temperature(str(temp))

            time.sleep(common.TEMPERATURE_SENSOR_SIMULATOR_SLEEP_TIME)

    def client(self):
        logging.info(f"Sensor Client {self.did} starting")

        try:
            while True:
                payload = self.measurement.to_dict()

                response = requests.post(
                    f"{common.CLOUD_API_URL}/sensor",
                    json=payload,
                    timeout=5
                )
                response.raise_for_status()

                logging.info(f"Temperatur sendt for {self.did}: {payload['value']}")

                time.sleep(common.TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME)

        except requests.RequestException as e:
            logging.error(f"Client-feil for {self.did}: {e}")

        logging.info(f"Client {self.did} finishing")

    def run(self):
        sim_thread = threading.Thread(target=self.simulator, daemon=True)
        sim_thread.start()

        client_thread = threading.Thread(target=self.client, daemon=True)
        client_thread.start()
