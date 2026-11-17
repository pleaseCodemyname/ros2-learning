# 구독: "/camera/image"
# 변환: 콜백에서 imgmsg_to_cv2(msg, "bgr8")
# 저장: cv2.imwrite("/tmp/frame.png", frame)
# 한 장만 받고 끝내기: 콜백 맨 끝에서 rclpy.shutdown()을 부르면 spin이 멈춤. 그 뒤 main에서 정리할 때는 try_shutdown()을 쓰면 두 번 꺼도 에러가 안남

import rclpy
import cv2
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class SaveFrame(Node):
    def __init__(self):
        super().__init__('save_frame')
        self.subscription = self.create_subscription(Image, "/camera/image", self.save_frame_callback, 10)
        self.bridge = CvBridge()

    def save_frame_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        cv2.imwrite("/tmp/frame.png", frame)
        self.get_logger().info(f"저장: {frame.shape}")
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    save_frame = SaveFrame()
    try:
        rclpy.spin(save_frame)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        save_frame.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()