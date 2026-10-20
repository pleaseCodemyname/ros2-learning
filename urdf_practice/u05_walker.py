import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from rclpy.executors import ExternalShutdownException


class Walker(Node):
    def __init__(self):
        super().__init__('walker')
        self.publisher_=self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.1, self.walker_callback)
        self.angle = 0.0
        self.direction = 1

    def walker_callback(self):
        msg = JointState()
        msg.name = ["base_to_right_leg", "base_to_left_leg"]
        msg.position = [self.angle, -self.angle]
        msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher_.publish(msg)
        self.angle +=0.05 * self.direction
        if self.angle > 0.5:
            self.direction = -1
        elif self.angle < -0.5:
            self.direction = 1


def main(args=None):
    rclpy.init(args=args)
    walker = Walker()
    try:
        rclpy.spin(walker)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        walker.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()