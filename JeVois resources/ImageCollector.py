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
        
        # Find the path to the first partition on any USB disk drive
        if not os.path.exists('/media/usb'):
            os.mkdir('/media/usb')
        # Try to mount the first available USB partition
        if not os.system('mount -t vfat /dev/sda1 /media/usb'):
            jevois.sendSerial("Mounted disk /dev/sda1 in /media/usb")
        elif not os.system('mount -t vfat /dev/sda2 /media/usb'):
            jevois.sendSerial("Mounted disk /dev/sda2 in /media/usb")
        elif not os.system('mount -t vfat /dev/sdb1 /media/usb'):
            jevois.sendSerial("Mounted disk /dev/sdb1 in /media/usb")
        elif not os.system('mount -t vfat /dev/sdb2 /media/usb'):
            jevois.sendSerial("Mounted disk /dev/sdb2 in /media/usb")
        else:
            jevois.sendSerial("No partitions found on the disk")
            raise RuntimeError("No USB disk partitions found")

        self.counter = 1
        while True:
            filename = os.path.join("JeVois captures", "take{}".format(self.counter))
            self.path = os.path.join("media","usb", filename)
            if not os.path.exists(self.path):
                break
            else:
                self.counter += 1
                
        # Create an ArUco marker detector:
        self.newsecond = 0

    # ###################################################################################################
    # Process function with GUI output (JeVois-Pro mode):
    def processGUI(self, inframe, helper):
        if self.foundUSB:
            # Start a new display frame, gets its size and also whether mouse/keyboard are idle:
            idle, winw, winh = helper.startFrame()

            # Draw full-resolution color input frame from camera. It will be automatically centered and scaled to fill the
            # display without stretching it. The position and size are returned, but often it is not needed as JeVois
            # drawing functions will also automatically scale and center. So, when drawing overlays, just use image
            # coordinates and JeVois will convert them to display coordinates automatically:
            x, y, iw, ih = helper.drawInputFrame("c", inframe, False, False)

            # Get the next camera image for processing (may block until it is captured), as greyscale:
            inimg = inframe.getCvBGRp()

            # Start measuring image processing time (NOTE: does not account for input conversion time):
            self.timer.start()

            date = datetime.datetime.now()
            file_exist = True
            c = 0
            interval = 1  # in seconds
            
            jevois.sendSerial("Now taking pictures every {} seconds ".format(interval))                  

            if not date.second % interval and self.newsecond != date.second:
                self.newsecond = date.second
                while True:
                    filename = os.path.join(self.path,"/capture_{:04d}-{:04d}".format(self.counter,c))
                    if os.path.exists(filename + ".jpg"):
                        c += 1
                    else:
                        filename = filename + ".jpg"
                        break

                # Encode the image data as a JPEG image
                # retval, buf = cv2.imencode('.jpg', inimg)
                # Write the compressed image data to disk if the directory still exists
                if os.path.exists(os.path.dirname(filename)):
                    with open(filename, 'wb') as f:
                        jevois.sendSerial("writing " + filename)
                        cv2.imwrite(filename, inimg)

                        # f.write(buf)
                else:
                    raise RuntimeError("USB removed")


            # Write frames/s info from our timer:
            fps = self.timer.stop()
            helper.iinfo(inframe, fps, winw, winh)

            # End of frame:
            helper.endFrame()
