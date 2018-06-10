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

fw._angle = {'straight': 82, 'left': 30, 'right': 130}


def single_turn(run_time):
	fw.turn_left()
	sleep(3)
	fw.turn_straight()
	sleep(run_time)

def spiral_move(run_time, turn_num):
	for i in range(turn_num):
		single_turn(run_time)

def main():
	bw.backward()
	bw.speed = 40
	for i in range(10):
		print('current front wheel angle parameter: {}'.format(fw._angle))
		turn_num = 4
		run_time = i + 0.5
		print('current loop number: {}, current run time: {}'.format(i, run_time))
		spiral_move(run_time, turn_num)
		print('this loop ends!')
	bw.stop()