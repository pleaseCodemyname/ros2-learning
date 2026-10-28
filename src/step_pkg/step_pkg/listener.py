import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(String, "/greeting", self.listener_callback, 10)

    def listener_callback(self, msg):
        self.get_logger().info(f"받음: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    listener = Listener()
    try:
        rclpy.spin(listener)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        listener.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()