# Outline
# -------
# Python MQTT Client sends and receives unlock commands along with secret key
# Raspberry Pi sends unlock signal to maglock
# Confirm unlock if possible
# Send unlock confirmation back via MQTT

import paho.mqtt.client as mqtt
import json
import time
import hashlib

class Cerberus(object):
	def __init__(self):
		# initialize the class that controls the brains of the lock
		print("initializing Cerberus.")
		self.reconnect_wait_time = 1
		self.secret_key = hashlib.md5("super secret door key").hexdigest()
		print("secret key: " + self.secret_key)
		self.thingfabric_info = {	
									"url": "q.thingfabric.com",
									"port": 1883,
									"keepalive": 10,
									"domain": "30c5c1103209c9df0eb5abf998fdf33a",
									"username": "256fd1ca-0cef-4cc0-8603-769a5fe78dfc",
									"password_hash": hashlib.md5("aa42b6c1-54c7-43b6-8764-ae83ba191d1b").hexdigest(),
									"inbound_topic": "/cerberus/inbound",
									"outbound_topic": "/cerberus/outbound"
								}
		self.initialize_mqtt_client()

	def initialize_mqtt_client(self):
		print("Initializing MQTT Client.")
		self.Client = mqtt.Client()
		self.Client.on_connect = self.on_connect
		self.Client.on_disconnect = self.on_disconnect
		self.Client.on_subscribe = self.on_subscribe
		self.Client.on_message = self.on_message
		self.Client.username_pw_set(self.thingfabric_info["username"], self.thingfabric_info["password_hash"])
		self.Client.connect(self.thingfabric_info["url"], self.thingfabric_info["port"], self.thingfabric_info["keepalive"])
		self.Client.loop_forever()

	def on_connect(self, client, userdata, flags, rc):
		if rc != 0:
			print("MQTT Client connection returned RC " + str(rc))
		else: 
			print("MQTT Client connected. (" + str(rc) + ")")
			self.reconnect_wait_time = 1
			self.Client.subscribe(self.thingfabric_info["domain"] + self.thingfabric_info["inbound_topic"])

	def on_disconnect(self, client, userdata, rc):
		print("Connection lost.")
		print("Retrying connection in " + str(self.reconnect_wait_time) + " seconds.")
		time.sleep(self.reconnect_wait_time)
		self.reconnect_wait_time = self.reconnect_wait_time * 2
		self.Client.connect(self.thingfabric_info["url"], self.thingfabric_info["port"], self.thingfabric_info["keepalive"])

	def on_subscribe(self, client, userdata, mid, granted_qos):
		print("Subscribed.")

	def on_message(self, client, userdata, message):
		print("Message received.")
		self.parse_mqtt(message.payload)

	def parse_mqtt(self, mqtt_payload):

		# look at MQTT message and decide what to do
		parsed_json = json.loads(mqtt_payload)


		# Assume two fields:
		# Command:  lock/unlock
		# Key:      keeps intrusive MQTT messages from unlocking the door (industrial espionage, bandits, spurned lovers, etc.)

		# Both these fields have to exist
		if "command" in parsed_json.keys() and "key" in parsed_json.keys():
			command = parsed_json["command"]
			key = parsed_json["key"]
			if key == self.secret_key:
				# Alright, we're safe.
				print("Secret key matches.")
				self.execute_command(command)
			else: 
				# INTRUDER
				print("Secret key mismatch.")
		else: 
			# Why are you even here?
			print("Incorrect message parameters.")

	def execute_command(self, command):
		print("Command: " + command)
		if command.lower() == 'lock':
			# We'll 'lock' the door
			self.lock_door()
		elif command.lower() == 'unlock':
			# We'll 'unlock' the door
			self.unlock_door()

	def lock_door(self):
		print("Locking door.")

		# Use Pi's 3.3V GPIO to switch the 24V MOSFET on. (0V -> 3.3V)

		pass

	def unlock_door(self):
		print("Unlocking door.")

		# Use Pi's 3.3V GPIO to switch the 24V MOSFET off. (3.3V -> 0V)

		pass

cerberus = Cerberus()