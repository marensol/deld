import tkinter as tk
from tkinter import ttk
import logging
import requests

from messaging import ActuatorState
import common


def lightbulb_cmd(state, did):
    new_state = state.get()
    logging.info(f"Dashboard: {new_state}")

    # Opprett et ActuatorState-objekt
    actuator_state = ActuatorState(did=did, state=new_state)

    try:
        # Send HTTP POST-forespørsel til sky-tjenesten
        response = requests.post(
            f"{common.CLOUD_API_URL}/actuator",
            json=actuator_state.to_dict(),
            timeout=5
        )
        response.raise_for_status()
        logging.info("Tilstand sendt til sky-tjenesten.")
    except requests.RequestException as e:
        logging.error(f"Feil ved sending til sky-tjenesten: {e}")


def init_lightbulb(container, did):
    lb_lf = ttk.LabelFrame(container, text=f'LightBulb [{did}]')
    lb_lf.grid(column=0, row=0, padx=20, pady=20, sticky=tk.W)

    # variable used to keep track of lightbulb state
    lightbulb_state_var = tk.StringVar(None, 'Off')

    on_radio = ttk.Radiobutton(lb_lf, text='On', value='On',
                               variable=lightbulb_state_var,
                               command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    on_radio.grid(column=0, row=0, ipadx=10, ipady=10)

    off_radio = ttk.Radiobutton(lb_lf, text='Off', value='Off',
                                variable=lightbulb_state_var,
                                command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    off_radio.grid(column=1, row=0, ipadx=10, ipady=10)
