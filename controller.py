from __future__ import print_function
from picar import front_wheels, back_wheels
import picar
import time
import cv2
#from pyzbar.pyzbar import decode


class CarController:
    def __init__(self):
        self.fw = front_wheels.Front_Wheels()
        self.fw._angle = {'straight': 82, 'left': 32, 'right': 132}
        self.bw = back_wheels.Back_Wheels()
        self.speed = 40
    
    def moveForward(self, t=0):
        """
        move the car forward, then stop
        """
        self.turnStraight()
        time.sleep(0.5)
        self.bw.backward()
        self.bw.speed = self.speed
        # make the car run for t second
        if t>0:
            time.sleep(t)
        self.bw.stop()
     
    def moveBackward(self, t=0):
        """
        move the car backward, then stop
        """
        self.turnStraight()
        time.sleep(0.5)
        self.bw.forward()
        self.bw.speed = self.speed
        # make the car run for t seconds
        if t>0: 
            time.sleep(t)
        self.bw.stop()

    def turnLeft(self, angle=0):
        """
        turn front wheel to the left
        """
        self.fw.turn_left()
        time.sleep(0.5)
    
    def turnRight(self, angle=0):
        """
        turn front wheel to the right
        """
        self.fw.turn_right()
        time.sleep(0.5)
    
    def turnStraight(self, angle=0):
        """
        turn front wheel straight
        """
        self.fw.turn_straight()
        time.sleep(0.5)

    def turnLeftNinty(self):
        """
        This function is car specific, and also related to friction
        Be sure to modify the code to fit your car and specific road condition
        The goal of the code is to make the car position stay the same
        while changing its "theta" to pi/2 (90degree)
        """
        self.fw.turn_straight()
        self.turnLeft()
        self.bw.backward()
        self.bw.speed = 40
        time.sleep(2)
        self.turnRight()
        self.bw.forward()
        self.bw.speed = 40
        time.sleep(2)
        self.turnStraight()

    def extract_barcode_location(self) :
        """
        This function tries to extract the barcode location
        information from the image by using pyzbar
        """
        # Load input image
        _, bgr_image = img.read()
        #barcode_info = decode(bgr_image)
        if barcode_info:
            # only return the barcode location info
            return barcode_info[0][2]
        else:
            return None