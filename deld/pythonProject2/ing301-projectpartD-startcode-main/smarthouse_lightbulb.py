import logging
import threading
import time
import requests

from messaging import ActuatorState
import common


class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState(did, 'False')

    def simulator(self):
        logging.info(f"Actuator {self.did} starting")
        while True:
            logging.info(f"Actuator {self.did}: {self.state.state}")
            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

    def client(self):
        logging.info(f"Actuator Client {self.did} starting")

        try:
            while True:
                response = requests.get(
                    f"{common.CLOUD_API_URL}/actuator/{self.did}",
                    timeout=5
                )
                response.raise_for_status()
                data = response.json()

                # Oppdater tilstanden
                new_state = data.get("state", "False")
                self.state = ActuatorState(did=self.did, state=new_state)

                logging.info(f"Actuator {self.did} oppdatert fra skyen: {new_state}")

                time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)

        except requests.RequestException as e:
            logging.error(f"Client-feil for {self.did}: {e}")

        logging.info(f"Client {self.did} finishing")

    def run(self):
        # Start simulator-tråd
        sim_thread = threading.Thread(target=self.simulator, daemon=True)
        sim_thread.start()

        # Start client-tråd
        client_thread = threading.Thread(target=self.client, daemon=True)
        client_thread.start()
