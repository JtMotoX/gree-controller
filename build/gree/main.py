#!/usr/bin/env python

from flask import Flask, json, request, jsonify
import requests
import jmespath
import os
import asyncio
import logging
import gree.controller
from copy import deepcopy

app = Flask(__name__)

logging.basicConfig(
    level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s"
)
_LOGGER = logging.getLogger(__name__)

@app.before_first_request
def before_first_request():
	global device
	device = asyncio.run(gree.controller.bind())

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
		old_device_info = deepcopy(asyncio.run(gree.controller.get_info(device)))
	except Exception as e:
		_LOGGER.error("{}: {}".format(type(e).__name__,e))
		return {"error": "There was an error getting the device info"}

	# DETERMINE THE CHANGES TO MAKE
	try:
		device = deepcopy(old_device_info)
		if mode == "off":
			device.power = False
		else:
			if mode == "cool":
				device.power = True
				device.mode = 1
			elif mode == "heat":
				device.power = True
				device.mode = 4
			else:
				_LOGGER.error("mode not supported: {}".format(str(mode)))
				return {"error": "mode not supported: {}".format(str(mode))}
			device.temperature_units = 1
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
