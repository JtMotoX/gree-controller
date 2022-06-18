#!/usr/bin/env python

from flask import Flask, json, request, jsonify
import requests
import jmespath
import os
import asyncio
import logging
from greeclimate.device import FanSpeed, Mode, TemperatureUnits
import gree.controller
from copy import deepcopy

app = Flask(__name__)

logging.basicConfig(
    level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s"
)
_LOGGER = logging.getLogger(__name__)

# RUN ON STARTUP
def app_startup():
	_LOGGER.debug("App starting . . .")
	global device
	try:
		device = asyncio.run(gree.controller.bind())
	except Exception as e:
		_LOGGER.error("{}: {}".format(type(e).__name__,e))
		return {"error": "There was an error binding to device"}

app_startup()

@app.route('/temperature-adjust', methods=['GET', 'POST'])
def temperature_adjust():
	global device
	# GET REQUEST DATA
	try:
		request_data = request.json
		mode = request_data["mode"]
		adjust = request_data["adjust"]
	except:
		return {"error": "You must pass the 'mode', 'temperature_adjust' in the POST request"}

	# GET DEVICE INFO BEFORE MAKING CHANGES
	try:
		bind_counter = 0
		old_device_info = False
		while old_device_info == False and bind_counter < 5:
			bind_counter += 1
			old_device_info = deepcopy(asyncio.run(gree.controller.get_info(device)))
			if old_device_info == False:
				if bind_counter > 1:
					_LOGGER.debug("Error getting device info. Going to try binding. (attempt {}".format(bind_counter))
				device = asyncio.run(gree.controller.bind())
	except Exception as e:
		_LOGGER.error("{}: {}".format(type(e).__name__,e))
		return {"error": "There was an error getting the device info"}

	# DETERMINE THE CHANGES TO MAKE
	try:
		device = deepcopy(old_device_info)
		if mode == "off":
			device.power = False
		elif mode == "toggle-power":
			device.power = not old_device_info.power
		else:
			if mode == "cool":
				device.power = True
				device.mode = Mode.Cool
			elif mode == "heat":
				device.power = True
				device.mode = Mode.Heat
			else:
				_LOGGER.error("mode not supported: {}".format(str(mode)))
				return {"error": "mode not supported: {}".format(str(mode))}
			device.temperature_units = TemperatureUnits.F
			device.target_temperature = old_device_info.target_temperature + int(adjust)
	except Exception as e:
		_LOGGER.error("{}: {}".format(type(e).__name__,e))
		return {"error": "There was an error determining the changes"}

	# SEND COMMANDS TO DEVICE
	try:
		asyncio.run(gree.controller.set_state(device))
	except Exception as e:
		_LOGGER.error("{}: {}".format(type(e).__name__,e))
		return {"error": "There was an error getting the device info"}

	# GET DEVICE INFO AFTER MAKING CHANGES
	try:
		new_device_info = deepcopy(asyncio.run(gree.controller.get_info(device)))
	except Exception as e:
		_LOGGER.error("{}: {}".format(type(e).__name__,e))
		return {"error": "There was an error getting the device info"}

	# SEND RESPONSE
	return {
		"old": {
			"power": old_device_info.power,
			"temperature": old_device_info.target_temperature
		},
		"new": {
			"power": new_device_info.power,
			"temperature": new_device_info.target_temperature
		}
	}


if __name__ == "__main__":
	app.run(host='0.0.0.0')
