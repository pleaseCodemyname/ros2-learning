import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from sensor_msgs.msg import JointState

class WheelSpinner(Node):
    def __init__ (self):
        super().__init__('wheel_spinner')
        self.publisher_=self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.1, self.wheel_spinner_callback)
        self.angle = 0.0

    def wheel_spinner_callback(self):
        msg = JointState()
        msg.name = ["base_to_right_wheel", "base_to_left_wheel"]
        msg.position = [self.angle, self.angle]
        msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher_.publish(msg)
        self.angle += 0.05            

        
def main(args=None):
    rclpy.init(args=args)
    wheel_spinner = WheelSpinner()
    try:
        rclpy.spin(wheel_spinner)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        wheel_spinner.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()

