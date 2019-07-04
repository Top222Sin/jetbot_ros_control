#!/usr/bin/env python

import  os
import  sys
import  tty, termios

import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

cmd = Twist()
pub = rospy.Publisher('jetbot_ros/cmd_raw', Twist, queue_size=1)


def keyboardLoop():
    rospy.init_node('teleop_read')
    rate = rospy.Rate(rospy.get_param('~hz', 1))
    
    walk_vel_ = rospy.get_param('walk_vel', 0.5)
    max_tv = walk_vel_

    print "Reading from keyboard"
    print "Use WASD keys to control the robot"
    print "Press Caps to move faster"
    print "Press q to quit"

    while not rospy.is_shutdown():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        old_settings[3] = old_settings[3] & ~termios.ICANON & ~termios.ECHO
        try :
            tty.setraw( fd )
            ch = sys.stdin.read( 1 )
        finally :
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if ch == 'w':
            max_tv = walk_vel_
            speed_left = 1
            speed_right = 1
            turn = 0
        elif ch == 's':
            max_tv = walk_vel_
            speed_left = -1
            speed_right = -1
            turn = 0
        elif ch == 'a':
            max_tv = walk_vel_
            speed_left = 0
            speed_right = 1
            turn = 1
        elif ch == 'd':
            max_tv = walk_vel_
            speed_left = 1
            speed_right = 0
            turn = -1
        elif ch == 'e':
            speed_left = 0
            speed_right = 0
            turn = -1
        elif ch == 'q':
            exit()
        else:
            max_tv = walk_vel_
            max_rv = yaw_rate_
            speed = 0
            turn = 0

        cmd.linear.x = speed_left * max_tv
        cmd.linear.y = speed_right * max_tv
        # cmd.angular.z = turn * max_rv
        pub.publish(cmd)
        rate.sleep()

def stop_robot():
    cmd.linear.x = 0.0
    cmd.angular.z = 0.0
    speed_left = 0
    speed_right = 0
    turn = 0
    pub.publish(cmd)

# def start():
#     global pub
#     rospy.init_node('teleop_read')
#     # Set rospy to exectute a shutdown function when exiting       
#     rate = rospy.Rate(rospy.get_param('~hz', 1))
#     rospy.Subscriber("/cmd_vel", Twist, callback)
#     rospy.spin()

if __name__ == '__main__':
    try:
        keyboardLoop()
    except rospy.ROSInterruptException:
        pass