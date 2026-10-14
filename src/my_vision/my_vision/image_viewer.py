import rclpy
import cv2
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class ImageViewer(Node):
    def __init__(self):
        super().__init__("image_viewer")
        self.bridge = CvBridge()
        self.topic = self.declare_parameter('topic', 'image').get_parameter_value().string_value # 해당 줄은 Subscriber를 만드는 줄 보다 위에 있어야함. 쓰기 전에 먼저 값을 받아 두어야 하기 때문
        self.subscription = self.create_subscription(Image, self.topic, self.image_view_callback, 10)
        self.get_logger().info('image view 시작됐다')
    
    def image_view_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        cv2.imshow('my viewer', frame)
        cv2.waitKey(1)
        self.get_logger().info(f'{frame.shape}', throttle_duration_sec=1.0)

def main(args=None):
    rclpy.init(args=args)
    image_viewer = ImageViewer()
    try:
        rclpy.spin(image_viewer)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        image_viewer.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()