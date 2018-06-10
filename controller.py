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

fw._angle = {'straight': 80, 'left': 15, 'right': 145}


def spiral_move(turn_angle, run_time):
	fw.turn(turn_angle)
	bw.backward()
	bw.speed = 60
	sleep(run_time)
	bw.stop()
	sleep(0.1)

def main():
	for i in range(30):
		print('current front wheel angle parameter: {}'.format(fw._angle))
		turn_angle = 20 + i*2
		run_time = i * 10
		print('current loop number: {}, current turning angle: {}, current run time: {}'.format(i, turn_angle, run_time))
		spiral_move(turn_angle, run_time)
		print('this loop ends!')
	bw.stop()