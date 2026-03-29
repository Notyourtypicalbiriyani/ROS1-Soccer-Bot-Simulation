#!/usr/bin/env python3
import rospy
import pygame
from geometry_msgs.msg import Twist

def main():
    rospy.init_node("dual_teleop")

    pub_blue = rospy.Publisher("/cmd_vel_blue", Twist, queue_size=1)
    pub_red  = rospy.Publisher("/cmd_vel_red", Twist, queue_size=1)

    pygame.init()
    pygame.display.set_mode((200, 200))
    clock = pygame.time.Clock()

    rospy.loginfo("Dual Teleop Started! Blue = WASD, Red = Arrow Keys")

    while not rospy.is_shutdown():
        pygame.event.pump()   # process key events

        keys = pygame.key.get_pressed()

        # ---------------------------
        # BLUE BOT (WASD)
        # ---------------------------
        blue_twist = Twist()

        if keys[pygame.K_w]:
            blue_twist.linear.x = 0.5
        elif keys[pygame.K_s]:
            blue_twist.linear.x = -0.5

        if keys[pygame.K_a]:
            blue_twist.angular.z = 0.8
        elif keys[pygame.K_d]:
            blue_twist.angular.z = -0.8

        # ---------------------------
        # RED BOT (ARROW KEYS)
        # ---------------------------
        red_twist = Twist()

        if keys[pygame.K_UP]:
            red_twist.linear.x = 0.5
        elif keys[pygame.K_DOWN]:
            red_twist.linear.x = -0.5

        if keys[pygame.K_LEFT]:
            red_twist.angular.z = 0.8
        elif keys[pygame.K_RIGHT]:
            red_twist.angular.z = -0.8

        # Publish both
        pub_blue.publish(blue_twist)
        pub_red.publish(red_twist)

        clock.tick(30)   # 30 Hz update

    pygame.quit()


if __name__ == "__main__":
    main()

