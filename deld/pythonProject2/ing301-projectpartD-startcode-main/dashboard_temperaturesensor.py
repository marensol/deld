import tkinter as tk
from tkinter import ttk

import logging
import requests

from messaging import SensorMeasurement
import common


def refresh_btn_cmd(temp_widget, did):
    logging.info("Temperature refresh")

    try:
        # Send GET-forespørsel til sky-tjenesten for å hente måling
        response = requests.get(
            f"{common.CLOUD_API_URL}/sensor/{did}",
            timeout=5
        )
        response.raise_for_status()

        # Anta at svaret er et JSON-objekt med en "value"-nøkkel
        data = response.json()
        sensor_measurement = SensorMeasurement(init_value=data.get("value", "-273.15"))

        logging.info(f"Mottatt temperatur: {sensor_measurement.value} °C")

    except requests.RequestException as e:
        logging.error(f"Feil ved henting av temperatur fra sky-tjenesten: {e}")
        sensor_measurement = SensorMeasurement(init_value="N/A")

    # Oppdater tekstfeltet i grensesnittet
    temp_widget['state'] = 'normal'
    temp_widget.delete(1.0, 'end')
    temp_widget.insert(1.0, sensor_measurement.value)
    temp_widget['state'] = 'disabled'


def init_temperature_sensor(container, did):
    ts_lf = ttk.LabelFrame(container, text=f'Temperature sensor [{did}]')
    ts_lf.grid(column=0, row=1, padx=20, pady=20, sticky=tk.W)

    temp = tk.Text(ts_lf, height=1, width=10)
    temp.insert(1.0, 'None')
    temp['state'] = 'disabled'
    temp.grid(column=0, row=0, padx=20, pady=20)

    refresh_button = ttk.Button(ts_lf, text='Refresh',
                                command=lambda: refresh_btn_cmd(temp, did))
    refresh_button.grid(column=1, row=0, padx=20, pady=20)
