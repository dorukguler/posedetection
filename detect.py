import cv2
import posemodule as pm

videoFeed = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = pm.PoseDetector()
while True:
    ret, frame = videoFeed.read()
    frame = detector.FindPose(frame)
    lmlist = detector.getpoints(frame)
    if len(lmlist) != 0:
        x1, x2 = lmlist[4][1], lmlist[29][1]
        y1, y2 = lmlist[4][2], lmlist[29][2]
        detector.draw_circle(frame, x1, y1, x2, y2)
        print(detector.goldenratios(frame, lmlist))
    cv2.imshow('Feed', frame)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

videoFeed.release()
cv2.destroyAllWindows()