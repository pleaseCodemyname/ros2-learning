import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from turtlesim.srv import Spawn

class Spawner(Node):
    def __init__(self):
        super().__init__('spawner')
        self.cli = self.create_client(Spawn, "/spawn")
        self.cli.wait_for_service()


def main(args=None):
    rclpy.init(args=args)
    spawner = Spawner()
    req = Spawn.Request(x=2.0, y=8.0, theta=0.0, name="b07")
    future = spawner.cli.call_async(req) # spawner = main에서 만든 노드 객체, .cli = __init__에서 self.cli에 저장한 client 객체, .call_async(req): client의 메서드. req를 /spawn 서비스로 보낸다.
    try:
        rclpy.spin_until_future_complete(spawner, future)
        name = future.result().name
        if name == '':
            spawner.get_logger().error("이름이 비었습니다")
        else:
            spawner.get_logger().info(f"이름: {name}")
    except(KeyboardInterrupt,ExternalShutdownException):
        pass
    finally:
        spawner.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()