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

fw._angle = {'straight': 90, 'left': 20, 'right': 160}

def spiral_move(turn_angle, run_time):
	fw.turn(turn_angle)
	bw.backward()
	bw.speed = 30
	sleep(run_time)
	bw.stop()

def main():
	for i in range(20):
		turn_angle = 20 + i
		run_time = 1 + i * 4
		print('current loop number: {}, current turning angle: {}, current run time: {}'.format(i))
		spiral_move(turn_angle, run_time)
		print('this loop ends!')