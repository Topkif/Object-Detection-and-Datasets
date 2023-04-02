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
import subprocess

class ImageCollector:
    # ###################################################################################################
    # Constructor

    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("timer", 100, jevois.LOG_INFO)
        self.interval = 1  # in seconds
        foundUSB = False
        
        if not os.path.exists("/media/JeVois_captures"):
            # all_partitions = os.popen("lsblk -o NAME,SIZE,MOUNTPOINT -x NAME | awk '{if ($2 ~ /[0-9]+G/) print $1}'").read().splitlines()
            all_partitions = os.popen('lsblk -o NAME,MOUNTPOINT -x NAME | awk \'$2 == "" {print $1}\'').read().splitlines()
            
            # print all partitions
            for p in all_partitions:
                jevois.sendSerial(p + ",")
                
            for partition in all_partitions:
                # if it contains "sd" like sda, sdb, ... and if it is not already mounted, try to mount this partition
                if "sd" in partition and not os.path.ismount("/dev/{partition}"):
                    # try for different file system types
                    jevois.sendSerial("trying to mount as VFAT/exfat partion " + partition)
                    result = subprocess.run(["sudo", "mount", "-t", "vfat", "/dev/{}".format(partition), "/media/"], capture_output=True) 
                    if result.returncode == 0: # success
                        jevois.sendSerial("mounted {}" .format(partition))
                        foundUSB = True
                        break
                    
                    jevois.sendSerial("trying to mount as NTFS partion " + partition)
                    result = subprocess.run(["sudo", "mount", "-t", "ntfs-3g", "/dev/{}".format(partition), "/media/"], capture_output=True) 
                    if result.returncode == 0: # success
                        jevois.sendSerial("mounted {}" .format(partition))
                        foundUSB = True
                        break
                    
                    # For other file systems, use the default mount command
                    jevois.sendSerial("trying to mount as FAT32/default partion " + partition)
                    result = subprocess.run(["sudo", "mount", "/dev/{}".format(partition), "/media/"], capture_output=True) 
                    if result.returncode == 0: # success
                        jevois.sendSerial("mounted {}" .format(partition))
                        foundUSB = True
                        break
            if not foundUSB:
                raise RuntimeError("No partitions found or no disk inserted")
        else:
            jevois.sendSerial("Write directory: /media/JeVois_captures")

        self.counter = 1
        while True:
            dirname = os.path.join("JeVois_captures", "take{}".format(self.counter))
            self.path = os.path.join("/media", dirname)
            if not os.path.exists(self.path):
                os.makedirs(self.path)
                break
            else:
                self.counter += 1

            jevois.sendSerial("Now taking pictures every {} seconds ".format(self.interval))                  

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
            count = 0
            while True:
                timestamp = date.strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(self.path, "capture_{}.jpg".format(str(timestamp)))
                if os.path.exists(filename):
                    count += 1
                    filename = os.path.join(self.path, "capture_{}({}).jpg".format(str(timestamp),str(count)))
                else:
                    count = 0
                    break

            if cv2.imwrite(filename, inimg):
                jevois.sendSerial("writing " + filename)
                with open(filename, 'rb') as f:
                    os.fsync(f.fileno())
                    f.flush()
                    f.close()
            else:
                raise RuntimeError("USB removed")

        # Write frames/s info from our timer:
        fps = self.timer.stop()
        helper.iinfo(inframe, fps, winw, winh)

        # End of frame:
        helper.endFrame()
        
        # headless mode
    def processNoUSB(self, inframe):
        # Get the next camera image for processing (may block until it is captured), as greyscale:
        inimg = inframe.getCvBGR()

        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()

        date = datetime.datetime.now()

        if not date.second % self.interval and self.newsecond != date.second:
            self.newsecond = date.second
            count = 0
            while True:
                timestamp = date.strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(self.path, "capture_{}.jpg".format(str(timestamp)))
                if os.path.exists(filename):
                    count += 1
                    filename = os.path.join(self.path, "capture_{}({}).jpg".format(str(timestamp),str(count)))
                else:
                    count = 0
                    break

            if cv2.imwrite(filename, inimg):
                jevois.sendSerial("writing " + filename)
                with open(filename, 'rb') as f:
                    os.fsync(f.fileno())
                    f.flush()
                    f.close()
            else:
                raise RuntimeError("USB removed")