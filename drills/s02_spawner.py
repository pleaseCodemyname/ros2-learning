import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from turtlesim.srv import Spawn

class Spawner(Node):
    def __init__(self):
        super().__init__('spawner')
        self.cli = self.create_client(Spawn, '/spawn')
        self.cli.wait_for_service()

def main(args=None):
    rclpy.init(args=args)
    spawner = Spawner()
    try:
        req = Spawn.Request(x = 2.0,y=2.0, theta = 0.0, name='shy2')
        future = spawner.cli.call_async(req)
        rclpy.spin_until_future_complete(spawner, future)
        name = future.result().name
        if name == '':
            spawner.get_logger().error("이미 있는 이름이라 실패")
        else:
            spawner.get_logger().info(future.result().name)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        spawner.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
