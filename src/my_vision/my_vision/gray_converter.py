import rclpy
import cv2
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class GrayConverter(Node):
    def __init__(self):
        super().__init__('gray_converter')
        self.bridge = CvBridge()
        self.publisher_ = self.create_publisher(Image, 'image_gray', 10)
        self.subscription = self.create_subscription(Image, 'image', self.gray_convert_callback, 10)
        self.get_logger().info("Gray Converter has been started")

    def gray_convert_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_msg = self.bridge.cv2_to_imgmsg(gray, 'mono8')
        self.get_logger().info(f'{frame.shape, gray.shape}', throttle_duration_sec=1.0)

        self.publisher_.publish(gray_msg)

def main(args=None):
    rclpy.init(args=args)
    gray_converter = GrayConverter()
    try:
        rclpy.spin(gray_converter)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        gray_converter.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()