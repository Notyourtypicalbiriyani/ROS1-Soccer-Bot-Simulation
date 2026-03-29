#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import numpy as np
import cv2
from cv_bridge import CvBridge
import time

class BallFollower:
    def __init__(self):
        rospy.init_node("ball_follower")

        self.bridge = CvBridge()
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        rospy.Subscriber("/soccerbot_cam/camera/image_raw", Image, self.image_callback)

        self.ball_last_seen = time.time()
        self.pushing = False
        self.reversing = False

        rospy.loginfo("Ball follower with pushing logic started!")
        rospy.spin()

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower = np.array([5, 120, 120])
        upper = np.array([25, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)

        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        twist = Twist()
        now = time.time()

        if len(contours) > 0:
            # Ball found
            c = max(contours, key=cv2.contourArea)
            (cx, cy), radius = cv2.minEnclosingCircle(c)
            cx, cy = int(cx), int(cy)

            h, w = frame.shape[:2]
            error_x = cx - w//2

            twist.angular.z = -error_x * 0.01

            if radius < 60:
                twist.linear.x = 0.4
            elif radius < 120:
                twist.linear.x = 0.2
            else:
                twist.linear.x = 0.0

            self.ball_last_seen = now
            self.pushing = False
            self.reversing = False

            rospy.loginfo("Targeting ball: cx=%d radius=%.1f", cx, radius)

        else:
            # Ball missing
            missing_time = now - self.ball_last_seen

            # ------------------------------------
            # PHASE 2: SHORT LOSS -> PUSH FORWARD
            # ------------------------------------
            if missing_time < 0.4:
                twist.linear.x = 0.3
                twist.angular.z = 0.0
                self.pushing = True
                rospy.loginfo("Pushing ball forward (short loss)...")

            # ------------------------------------
            # PHASE 3: REVERSE TO REVEAL BALL
            # ------------------------------------
            elif missing_time < 0.8:
                twist.linear.x = -0.2
                twist.angular.z = 0.0
                self.reversing = True
                rospy.loginfo("Reversing to uncover ball...")

            # ------------------------------------
            # PHASE 4: Search mode (rotate)
            # ------------------------------------
            else:
                twist.angular.z = 0.5
                twist.linear.x = 0.0
                rospy.loginfo("Searching...")

        self.cmd_pub.publish(twist)

        cv2.imshow("mask", mask)
        cv2.imshow("camera", frame)
        cv2.waitKey(1)

if __name__ == "__main__":
    BallFollower()

