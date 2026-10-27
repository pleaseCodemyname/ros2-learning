import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String

class Numberer(Node):
    def __init__(self):
        super().__init__('numberer')
        self.subscription = self.create_subscription(String, "/greeting", self.numberer_callback, 10)
        self.publisher_ = self.create_publisher(String, "/numbered",10)
        self.count = 0

    def numberer_callback(self, msg):
        self.count +=1
        out = String()
        out.data = f"{self.count}: {msg.data}"
        self.publisher_.publish(out)
    

def main(args=None):
    rclpy.init(args=args)
    numberer = Numberer()
    try:
        rclpy.spin(numberer)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        numberer.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()



