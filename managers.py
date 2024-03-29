import cv2
import mediapipe as mp
import time
import numpy as np

class WindowManager(object):
    def __init__(self, mirror=True):
        self._capture = cv2.VideoCapture(0)
        self._windowName = 'NewWindow'
        self._enteredFrame = False
        self._frame = None
        self._isWindowCreated = False
        self._channel = 0
        self._framesElapsed = 0
        self._startTime = None
        self._fpsEstimate = None
        self._mirror = mirror
        self._isWindowCreated = False


    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve(self._frame, self.channel)
        return self._frame

    def enterFrame(self):
        assert not self._enteredFrame, \
            'previous enterFrame() had no matching exitFrame()'
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()
    def exitFrame(self):
        """Draw to the window. Write to files. Release the
         frame."""

        # Check whether any grabbed frame is retrievable.
        # The getter may retrieve and cache the frame.

        if self.frame is None:
            self._enteredFrame = False
            return
        # Update the FPS estimate and related variables.
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
            self._framesElapsed += 1

        # Draw to the window, if any.
        if self._isWindowCreated is not False:
            if self._mirror:
                self.show(self._frame)

                # scale_percent = 40  # percent of original size
                # width = int(self._frame.shape[1] * scale_percent / 100)
                # height = int(self._frame.shape[0] * scale_percent / 100)
                # dim = (width, height)
                # mirroredFrame = cv2.resize(self._frame, dim, interpolation=cv2.INTER_AREA)
                #
                #
                # cv2.imshow('new', mirroredFrame)

            else:
                cv2.imshow(self._windowName, (self.frame))


        self._frame = None
        self._enteredFrame = False
    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True

    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False

    def processEvents(self):
        keycode = cv2.waitKey(1)
        if keycode != -1:
            self.onKeypress(keycode)

    def show(self, frame):
        frame = np.fliplr(frame)
        cv2.imshow(self._windowName, (frame))

    def onKeypress(self, keycode):
        """Handle a keypress.
        space -> Take a screenshot.
        tab -> Start/stop recording a screencast.
        escape -> Quit.
        """
        if keycode == 27:
            self.destroyWindow()


