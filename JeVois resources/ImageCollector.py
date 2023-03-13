import pyjevois
if pyjevois.pro:
    import libjevoispro as jevois
else:
    import libjevois as jevois
import cv2
import numpy as np
import os.path
import datetime
import os


class ImageCollector:
    # ###################################################################################################
    # Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("timer", 100, jevois.LOG_INFO)
        self.foundUSB = False
        self.c = 0
        self.interval = 1  # in seconds

        # Find the largest FAT32 partition on the disk
        mount_cmd = "sudo parted -l | grep -i fat32 | sort -k3nr | head -n1 | awk '{print $1}'"
        partition = os.popen(mount_cmd).read().strip()

        if partition:
            # Check if /media/usb exists, if not create it
            if not os.path.exists('/media/usb'):
                os.mkdir('/media/usb')
                
        # If not already mounted
        disks = os.popen('mount').read()
        # Mount the disk in FAT32 format to /media/usb
        # 
        # 
        # 
        # TODO faire marcher ce test:        
        if not "/dev/sda1" in disks or not "/dev/sda2" in disks or not "/dev/sdb1" in disks or not "/dev/sdb2" in disks :
            if not os.system('mount -t vfat /dev/sda1 /media/usb'):
                jevois.sendSerial("Mounted disk /dev/sda1 in /media/usb")
                self.foundUSB = True
            elif not os.system('mount -t vfat /dev/sda2 /media/usb'):
                jevois.sendSerial("Mounted disk /dev/sda2 in /media/usb")
                self.foundUSB = True
            elif not os.system('mount -t vfat /dev/sdb1 /media/usb'):
                jevois.sendSerial("Mounted disk /dev/sdb1 in /media/usb")
                self.foundUSB = True
            elif not os.system('mount -t vfat /dev/sdb2 /media/usb'):
                jevois.sendSerial("Mounted disk /dev/sdb2 in /media/usb")
                self.foundUSB = True
            else:
                raise RuntimeError("No partitions found on the disk")
        else:
            jevois.sendSerial("Disk already mounted. Proceeding")

        self.counter = 1
        while True:
            dirname = os.path.join("JeVois_captures", "take{}".format(self.counter))
            self.path = os.path.join("/media","usb", dirname)
            if not os.path.exists(self.path):
                os.makedirs(self.path)
                break
            else:
                self.counter += 1

            jevois.sendSerial("Now taking pictures every {} seconds ".format(self.interval))                  

        # Create an ArUco marker detector:
        self.dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        self.params = cv2.aruco.DetectorParameters_create()
        self.newsecond = 0

    # ###################################################################################################
    # Process function with GUI output (JeVois-Pro mode):
    def processGUI(self, inframe, helper):
        # Start a new display frame, gets its size and also whether mouse/keyboard are idle:
        idle, winw, winh = helper.startFrame()

        # Draw full-resolution color input frame from camera. It will be automatically centered and scaled to fill the
        # display without stretching it. The position and size are returned, but often it is not needed as JeVois
        # drawing functions will also automatically scale and center. So, when drawing overlays, just use image
        # coordinates and JeVois will convert them to display coordinates automatically:
        x, y, iw, ih = helper.drawInputFrame("c", inframe, False, False)

        # Get the next camera image for processing (may block until it is captured), as greyscale:
        inimg = inframe.getCvBGR()

        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()

        date = datetime.datetime.now()

        if not date.second % self.interval and self.newsecond != date.second:
            self.newsecond = date.second
            while True:
                filename = os.path.join(self.path, "capture_{:04d}-{:04d}.jpg".format(self.counter,self.c))
                if os.path.exists(filename):
                    self.c += 1
                else:
                    break

            retval, buf = cv2.imencode('.jpg', inimg)
            if os.path.exists(os.path.dirname(filename)):
                with open(filename, 'wb') as f:
                    jevois.sendSerial("writing " + filename)
                    f.write(buf)
            else:
                raise RuntimeError("USB removed")

        # Write frames/s info from our timer:
        fps = self.timer.stop()
        helper.iinfo(inframe, fps, winw, winh)

        # End of frame:
        helper.endFrame()
