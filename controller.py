from __future__ import print_function
from picar import front_wheels, back_wheels
import picar
import time
import cv2
#from pyzbar.pyzbar import decode


class CarController:
    def __init__(self):
        self.fw = front_wheels.Front_Wheels()
        self.fw._angle = {'straight': 75, 'left': 32, 'right': 132}
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
        time.sleep(1)
    
    def turnRight(self, angle=0):
        """
        turn front wheel to the right
        """
        self.fw.turn_right()
        time.sleep(1)
    
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
        self.bw.stop()
        self.fw.turn_straight()
        self.turnLeft()
        self.bw.backward()
        self.bw.speed = 40
        time.sleep(3)
        self.bw.stop()
        self.turnRight()
        self.bw.forward()
        self.bw.speed = 40
        time.sleep(1.6)
        self.bw.stop()
        self.turnStraight()
        self.bw.forward()
        self.bw.speed = 40
        time.sleep(0.5)
        self.bw.stop()

    def moveRectangle(self, t):
        self.moveForward(t)
        self.turnLeftNinty()
        self.moveForward(t+0.8)
        self.turnLeftNinty()
        self.moveForward(t+0.4)
        self.turnLeftNinty()
        self.moveForward(t+0.2)
        self.turnLeftNinty()
        self.bw.stop()


    def moveMultipleRectange(self, num):
        for i in range(num):
            t = i + 2
            print('current run time is {}'.format(t))
            self.moveRectangle(t)


    def extract_barcode_location(self) :
        """
        This function tries to extract the barcode location
        information from the image by using pyzbar
        """
        # Load input image
        _, bgr_image = img.read()
        barcode_info = decode(bgr_image)
        if barcode_info:
            # only return the barcode location info
            return barcode_info[0][2]
        else:
            return None

    def drive_towards_barcode(self):
        """
        This function tries to make the car drive towards barcode
        in a straight line
        The barcode is used to help the car to follow the path (straight line)
        as well as stop at target position
        """
        # BW_MODE 1: moving forward
        # BW_MODE 0: moving backward
        BW_MODE = 1
        fw_angle = 90

        print "Begin!"
        while True:
            left = 0            # initialize left to be 0
            top = 0             # initialize top to be 0
            width = 0           # initialize width to be 0
            height = 0          # initialize height to be 0

            # try taking 10 images because pyzbar is not so consistent
            # extract barcode location when we manage to get one barcode detected
            for i in range(10):
                barcode_location = self.extract_barcode_location()
                # check if barcode is detecte
                if barcode_location:
                    #print "barcode found!"
                    #print(barcode_location)
                    left = barcode_location[0]
                    top = barcode_location[1]
                    width = barcode_location[2]
                    height = barcode_location[3]
                    break

            """
            If barcode is not found, keep moving forward or backward
            """
            if not barcode_location:
                # if the barcode could not be detected
                # keep moving the car forward
                if BW_MODE == 1:
                    self.bw.backward()
                else:
                    self.bw.forward()
                self.bw.speed = self.speed
                print "Couldn't detect barcode! backwheel keep running"
                sleep(0.3)

            # here we start to deal with cases where we could detect barcode
            else: 
                ################################################################
                """
                First utilize barcode to detect whether the car leaning towards left or right
                """
                # deal with case where barcode is on the left side of the image
                if left + width/2 > MIDDLE_POS + MIDDLE_TOLERANT:
                    print "The car is leaning towards the left!"
                    # turn the steering angle to the right slightly
                    fw_angle += 0.2
                    self.fw.turn(fw_angle)
                    sleep(0.2)
                # deal with case where barcode is on the right side of the image
                elif left + width/2 < MIDDLE_POS - MIDDLE_TOLERANT:
                    print "The car is leaning towards the right!"
                    # turn the steering angle to the left slightly
                    fw_angle -= 0.2
                    self.fw.turn(fw_angle)
                    sleep(0.2)
                else:
                    print "The car is right on track!"
                #################################################################
                """
                Next, utilize barcode to detect whether the car has reached target position
                """
                # deal with cases where barcode size in the image is larger than expected
                # the pyzbar is not so sensitive
                # this case might happen when pyzbar fails a couple of times
                # and now the car has passed target position
                # we need to move the car backward
                if width > BARCODE_WIDTH + MIDDLE_TOLERANT:
                    print "Width is larger than expected! Start backwarding!"
                    # moving back
                    self.bw.backward()
                    BW_MODE = 0
                    self.bw.speed = motor_speed
                    sleep(0.2)
                # deal with cases where barcode size is smaller than expected
                # this means the car still hasn't reached target position
                # we need to move the car forward
                elif width < BARCODE_WIDTH - MIDDLE_TOLERANT:
                    print "Width is smaller than expected! Start forwarding!"
                    self.bw.forward()
                    BW_MODE = 1
                    self.bw.speed = motor_speed
                    sleep(0.2)
                # stop when we have reached target position
                # also get out of the while loop
                else:
                    print "find it!"
                    self.turnStraight()
                    bw.stop()
                    break
            bw.stop()
            sleep(0.1)