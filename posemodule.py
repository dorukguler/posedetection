#önce importlar
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
from math import sqrt
#initialize mpos

class PoseDetector():
    def __init__(self):
        self.mpDraw=mp.solutions.drawing_utils
        self.mpPose=mp.solutions.pose
        self.pose=self.mpPose.Pose()
        self.x1=None
        self.x2=None
        self.y1=None
        self.y2=None


            # print(end-start)

    def FindPose(self, frame, draw=True):
        self.detected = self.pose.process(frame)
        if self.detected.pose_landmarks:
            if draw:
             self.mpDraw.draw_landmarks(frame,self.detected.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return frame

    def getpoints(self,frame,draw=True):
        lmlist=[]
        if self.detected.pose_landmarks:
            for id,lm in enumerate(self.detected.pose_landmarks.landmark):
                h,w,c=frame.shape
                cx,cy=int(lm.x*w), int(lm.y*h)
                lmlist.append([id,cx,cy])
                if draw:#mavi noktaları çiziyoruz
                    cv2.circle(frame, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        return lmlist

    def draw_circle(self, frame, x1, y1, x2, y2):
        centerx = (abs(x2 + x1)) // 2
        centery = (abs(y2 + y1)) // 2
        coordinates = (centerx, centery)
        Distance = sqrt((centerx - x1) ** 2 + (centery - y1) ** 2)
        Distance = sqrt((centerx - x1) ** 2 + (centery - y1) ** 2) * 1.25
        # radius=(abs(centerx-x2)**2+abs(centery-y2)**2)**1/2
        cv2.circle(frame, coordinates, int(Distance), (0, 255, 0), 5)

        return centerx, centery, x1, x2, y1, y2, Distance

    def goldenratios(self,frame,goldenlist):
        leftarmfullx=abs(goldenlist[16][1]-goldenlist[14][1])
        leftarmfully=abs(goldenlist[16][2]-goldenlist[14][2])
        leftfulllength= sqrt(leftarmfullx ** 2 + leftarmfully ** 2)
        leftarmhalfx=abs(goldenlist[14][1]-goldenlist[12][1])
        leftarmhalfy=abs(goldenlist[14][2]-goldenlist[12][2])
        lefthalflen=sqrt(leftarmhalfx ** 2 + leftarmhalfy ** 2)
        golden_ratio = int(leftfulllength/lefthalflen)
        cv2.putText(frame, str(golden_ratio),(70,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 2, cv2.LINE_8)
        return golden_ratio

    def waist_body_ratio(self,frame,goldenlist):
        leftarmfullx=abs(goldenlist[30][1]-goldenlist[6][1])
        leftarmfully=abs(goldenlist[30][2]-goldenlist[6][2])
        leftfulllength= sqrt(leftarmfullx ** 2 + leftarmfully ** 2)
        leftarmhalfx=abs(goldenlist[30][1]-goldenlist[24][1])
        leftarmhalfy=abs(goldenlist[30][2]-goldenlist[24][2])
        lefthalflen=sqrt(leftarmhalfx ** 2 + leftarmhalfy ** 2)
        theratio=leftfulllength/lefthalflen
        formatted_ratio = "{:.3f}".format(theratio)
        cv2.putText(frame,str(formatted_ratio),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(200,255,255),1,cv2.LINE_AA,bottomLeftOrigin= False)
        return formatted_ratio

    def resize(self, frame, resize):
        scale_percent = resize  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame.resize()
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        frame = np.array(frame).shape
        return frame
    def findratio(self,goldenlist,merkez,uzaknokta,yakınnokta):
        leftarmfullx = abs(goldenlist[merkez][1] - goldenlist[uzaknokta][1])
        leftarmfully = abs(goldenlist[merkez][2] - goldenlist[uzaknokta][2])
        leftfulllength = sqrt(leftarmfullx ** 2 + leftarmfully ** 2)
        leftarmhalfx = abs(goldenlist[merkez][1] - goldenlist[yakınnokta][1])
        leftarmhalfy = abs(goldenlist[merkez][2] - goldenlist[yakınnokta][2])
        lefthalflen = sqrt(leftarmhalfx ** 2 + leftarmhalfy ** 2)
        theratio = leftfulllength / lefthalflen
        formatted_ratio = "{:.3f}".format(theratio)
        return formatted_ratio

