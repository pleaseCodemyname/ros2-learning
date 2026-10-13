import rclpy
import cv2
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class ImageView(Node):
    def __init__(self):
        super().__init__("image_viewer")
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(Image, 'image', self.image_view_callback, 10)
        self.get_logger().info('image view 시작됐다')
    
    def image_view_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        cv2.imshow('my viewer', frame)
        cv2.waitKey(1)
        self.get_logger().info(f'{frame.shape}', throttle_duration_sec=1.0)

def main(args=None):
    rclpy.init(args=args)
    image_view = ImageView()
    try:
        rclpy.spin(image_view)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        image_view.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()