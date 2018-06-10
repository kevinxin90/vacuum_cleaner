from __future__ import print_function
from time import sleep

###############################################################
#This part controls the front wheel and backwheel
###############################################################
from picar import front_wheels, back_wheels

# bw will handle all the movements for backwheel
# backwheel controls the speed and direction(moving forward or backward)
bw = back_wheels.Back_Wheels()
# fw will handle all the movements for frontwheel
# front wheel controls the angle while the vehicle turns
fw = front_wheels.Front_Wheels()

fw._angle = {'straight': 80, 'left': 20, 'right': 140}


def spiral_move(run_time):
	# first left turn
	fw.turn_left()
	sleep(2.5)
	fw.turn_straight()
	sleep(run_time)
	# second left turn
	fw.turn_left()
	sleep(2.5)
	fw.turn_straight()
	sleep(run_time)
	# third left turn
	fw.turn_left()
	sleep(2.5)
	fw.turn_straight()
	sleep(run_time)
	# fourth left turn
	fw.turn_left()
	sleep(2.5)
	fw.turn_straight()
	sleep(run_time)

def main():
	bw.backward()
	bw.speed = 40
	for i in range(30):
		print('current front wheel angle parameter: {}'.format(fw._angle))
		run_time = i * 2
		print('current loop number: {}, current run time: {}'.format(i, run_time))
		spiral_move(run_time)
		print('this loop ends!')
	bw.stop()