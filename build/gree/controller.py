#!/usr/bin/env python3

import argparse
import asyncio
import logging
import sys
import traceback

from greeclimate.device import Device, DeviceInfo
from greeclimate.discovery import Discovery, Listener

async def bind():
	logging.debug("Searching for device . . .")
	discovery = Discovery()
	for device_info in await discovery.scan(wait_for=5):
		try:
			device = Device(device_info)
			logging.debug("Binding device . . .")
			await device.bind() # Device will auto bind on update if you omit this step
			return device
		except:
			logging.error("Unable to bind to gree device: %s", device_info)
			continue

async def get_info(device):
	logging.debug("Getting device info . . .")
	try:
		await device.update_state()
		return device
	except Exception as e:
		logging.error("{}: {}".format(type(e).__name__,e))
		logging.debug(traceback.format_exc())
		return False

async def set_state(device):
	logging.debug("Sending commands to device . . .")
	try:
		await device.push_state_update()
		return True
	except Exception as e:
		logging.error("{}: {}".format(type(e).__name__,e))
		return False
