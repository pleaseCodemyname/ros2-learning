import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException

class DrillOne(Node):
    def __init__(self):
        super().__init__('drill_one') # 노드 이름
        self.get_logger().info('drill_one 시작')


def main(args=None):
    rclpy.init(args=args)
    drill_one = DrillOne()
    try:
        rclpy.spin(drill_one)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        drill_one.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()