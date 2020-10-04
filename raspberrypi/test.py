#!/usr/bin/env python
import string
import random
import re
import os
import sys
import time
import threading
import logging.config
from evdev import InputDevice
from evdev import util
from keymap import keys
from payload import Payload

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)
finish = threading.Event()

def check_arg():
	if len(sys.argv) != 2:
		logger.error("usage: python soroban.py TargetURL")
		sys.exit()
	global host_id, url
	host_id = format(random.randrange(10000),"04")
	url = sys.argv[1].strip()

def discover_devices():
	devices = [InputDevice(path) for path in util.list_devices(input_device_dir='/dev/input')]
	devices = [device for device in devices if device.phys[-6:] == 'input0']
	return devices

def make_threadlist(devices):
        threadlist = list()
	thread_num = 0
        for device in devices:
                thread = make_thread(device)
                threadlist.append(thread)
        return threadlist

def make_thread(device,):
        logger.info(device.phys)
        thread  = threading.Thread(target=wait_input, args=([device]))
        thread.daemon = True
        return thread

def wait_input(device):
	keyboard_id = ""
	# if using thread name: threading.current_thread().name[-1:]
	q_sheet, q_number = "0", "0"
	is_first = True
	while True:
		logger.debug("read device")
		answer = read_answer(device)
		function = decide_function(answer)
		if is_first:
			keyboard_id = answer
			is_first = False
			logger.info("keyboard id is set: %s" % keyboard_id)
			continue
		if function == 1:
			logger.info("len == 0")
		elif function == 2:
			logger.info("is finish")
			finish.set()
			return
		elif function == 3:
			q_sheet = re.sub("\D","",answer)
			logger.info("question sheet number is set: %s" % q_sheet)
		elif function == 4:
			q_sheet = str(int(q_sheet) + 1)
			logger.info("next question sheet number is set: %s" % q_sheet)
		elif function == 5:
			q_number = re.sub("\D","",answer)
			logger.info("question number is set: %s" % q_number)
		elif function == 6:
			q_number = str(int(q_number) + 1)
			logger.info("next question number is set: %s" % q_number)
		else:
			answer = re.sub("\D","",answer)
			payload = Payload(url, host_id, keyboard_id, q_sheet, q_number, answer)
			r = payload.send()
			logger.info("payload.send(): %s" % r)

def read_answer(device):
        answer = ''
        for event in device.read_loop():
                if event.type==1 and event.value==1 and event.code in keys:
                        if event.code==96:
                                return answer
                        answer += keys[event.code]
        return None

def decide_function(answer):
	if len(answer) == 0:
		return 1
	if len(answer) == 8 and all([n == '0' for n in answer]):
		return 2
        if len(answer) == 1:
		if answer[0] == '/':
			return 3
                elif answer[0] == '*':
			return 5
	if len(answer) > 1:
		if answer[0] == '/':
			if answer[1] == "/":
				return 4
			else:
				return 3
		elif answer[0] == '*':
		        if answer[1] == "*":
                                return 6
                        else:
                                return 5
        return 0

def main():
	try:
		check_arg()
		devices = discover_devices()
		threadlist = make_threadlist(devices)

		for thread in threadlist:
			thread.start()
			logger.debug('thread start: ')

		while not finish.is_set():
			time.sleep(1)

		print 'finish'

	except:
		import traceback
		logger.error(traceback.print_exc())

if __name__ == '__main__':
	main()
