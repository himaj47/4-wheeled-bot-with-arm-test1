#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class jointStatePub(Node):
    def __init__(self):
        super().__init__("joint_state_pub")
        self.name = ["base_arm_base_joint","base_arm_first_joint","second_arm_link_joint","arm_link_second_rev_joint","base_right_wheel_joint","base_left_wheel_joint", "gripper_right_joint", "gripper_left_joint", "base_front_left_wheel_joint", "base_front_right_wheel_joint"]
        #gripper and arm base value clockwise rest -ve clockwise 
        self.state_publisher = self.create_publisher(JointState,"/joint_states",10)

        # end effector matrix:
        # self.H = [[math.cos(3.14), -math.sin(3.14), 0.0, 0.2],
        #           [math.sin(3.14), math.cos(3.14), 0.0, 0.1],
        #           [0.0, 0.0, 1.0, 0.15],
        #           [0.0, 0.0, 0.0, 1.0]]
        
        self.x = 0.2
        self.y = 0.1
        self.z = 0.2

        self.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.velocity = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.effort = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        self.arm_base_rot = math.tan(self.y/self.x)
        self.initial_pos_arm_base = self.position[0]
        self.kp = 1

        # self.get_logger().info('JointState published.')
        self.control_loop = self.create_timer(0.01,self.loopCallBack)

    def loopCallBack(self):
        arm_base_err = self.kp*(self.arm_base_rot - self.initial_pos_arm_base)

        self.get_logger().info("error = " + str(arm_base_err))
        self.get_logger().info("initial_pos_arm_base = " + str(self.initial_pos_arm_base))
        if(arm_base_err > 0.0):
            self.get_logger().info("reached position")
            self.initial_pos_arm_base += 0.0001
            self.position[0] += self.initial_pos_arm_base

        data = JointState()
        data.header.stamp = self.get_clock().now().to_msg()
        data.name = self.name
        data.position = self.position
        data.velocity = self.velocity
        data.effort = self.effort
        self.state_publisher.publish(data)

def main(args=None):
    rclpy.init(args=args)
    node = jointStatePub()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()