#!/usr/bin/env python

import sys
import threading
import nxt.locator
from nxt.motor import *
from nxt.sensor import *

class thread_wait( threading.Thread ):
	def __init__( self, condition, action):
		threading.Thread.__init__( self )
		self.condition = condition
		self.action = action

	def run( self ):
		while not self.condition():
			sleep(0.1)
		self.action()


class MazeBot:
	def __init__(self):
		print 'Looking for brick 7 ...'
		sock = nxt.locator.find_one_brick(host='00:16:53:08:3D:31',
						name='NXT')
		print 'Found brick 7 or timed-out ...'
		if sock:
			print 'Connecting to the brick ...'
			self.brick = sock.connect()
			print 'Connected to the brick or timed-out ...'
			if self.brick:
				self.drive			= nxt.motor.Motor(self.brick, PORT_B)
				self.turn			= nxt.motor.Motor(self.brick, PORT_A)
				self.wall_contact	= TouchSensor(self.brick, PORT_3)
				self.wall_close	= TouchSensor(self.brick, PORT_1)
				self.front_contact= TouchSensor(self.brick, PORT_2)
				self.sound			= SoundSensor(self.brick, PORT_4)

				self.sensor_lock	= threading.Lock()

				kill_switch_thread = thread_wait( self.get_sound, self.stop )
				kill_switch_thread.start()

			else:
				print 'Could not connect to NXT brick'
		else:
			print 'No NXT bricks found'

	def go(self, speed= 127):
		self.sensor_lock.acquire()
		self.drive.run(speed)
		self.sensor_lock.release()

	def spin(self, speed=-127):
		self.sensor_lock.acquire()
		self.turn.run(speed)
		self.sensor_lock.release()
	
	def stop(self):
		self.sensor_lock.acquire()
		self.drive.stop()
		self.turn.stop()
		self.sensor_lock.release()

	def suicide(self):
		#print "Dying."
		self.stop()
		sleep(1)

	def has_wall_contact(self):
		pass
	
	def get_sound(self):
		pass
		
	
def run_maze(side = -1):
	bill = MazeBot( )
	try:
		pass
	finally:
		bill.stop()
	
def test():
	bob = MazeBot()
	sleep(3)
	bob.spin()
	sleep(5)
	bob.stop()
	exit()
	
if __name__ == "__main__":
	test()

