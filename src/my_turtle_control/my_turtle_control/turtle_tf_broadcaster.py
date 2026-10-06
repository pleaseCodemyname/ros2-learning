import math
import rclpy
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose
from rclpy.node import Node

class TurtleTFBroadcaster(Node):
    def __init__(self):
        super().__init__('turtle_tf_broadcaster')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.subscription = self.create_subscription(
                    Pose,
                    'turtle1/pose',
                    self.pose_callback,
                    10)
        self.get_logger().info('TF Broadcaster Node has been started.')

    def pose_callback(self, msg):
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'turtle1'

        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0

        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = math.sin(msg.theta / 2.0)
        t.transform.rotation.w = math.cos(msg.theta / 2.0)

        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    turtle_tf_broadcaster = TurtleTFBroadcaster()
    try:
        rclpy.spin(turtle_tf_broadcaster)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        turtle_tf_broadcaster.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()