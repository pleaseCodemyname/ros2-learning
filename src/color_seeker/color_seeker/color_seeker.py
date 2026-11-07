# Pub(무엇을 내보내나?): 속도/회전 명령, 인터페이스: geometry_msgs/msg/Twist
# Sub(무엇을 알아야 하나?): 로봇 카메라 사진, 인터페이스: sensor_msgs/msg/Image
# 타미어(받는 것 없이 반복할 일이 있나?): 없음, 사진이 올 때마다(약 24번/초) 콜백에서 판단하면 됨

import rclpy 
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image

