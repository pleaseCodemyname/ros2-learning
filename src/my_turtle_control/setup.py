from setuptools import find_packages, setup

package_name = 'my_turtle_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', 
            ['launch/turtle_control_launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shy',
    maintainer_email='545austin@naver.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'circle_publisher = my_turtle_control.circle_publisher:main',
            'pose_subscriber = my_turtle_control.pose_subscriber:main',
            'wall_avoider = my_turtle_control.wall_avoider:main',
            'turtle_tf_broadcaster = my_turtle_control.turtle_tf_broadcaster:main',
        ],
    },
)
