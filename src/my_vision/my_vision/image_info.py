import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import Image

class ImageInfo(Node):
    def __init__(self):
        super().__init__("image_info")
        self.subscription = self.create_subscription(
            Image,
            'image',
            self.image_callback,
            10
        )
        self.get_logger().info("Image Info is getting started")

    def image_callback(self, msg):
        height = msg.height
        width = msg.width
        encoding = msg.encoding
        self.get_logger().info(f"세로는 {height}, 가로는 {width}, 인코딩은 {encoding}", throttle_duration_sec = 1.0)


def main(args=None):
    rclpy.init(args=args)
    image_info = ImageInfo()
    try:
        rclpy.spin(image_info)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        image_info.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()