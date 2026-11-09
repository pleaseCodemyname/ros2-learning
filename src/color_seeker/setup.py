from setuptools import find_packages, setup

package_name = 'color_seeker'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/color_seeker/launch', # 설치될 폴더
            ['launch/color_seeker_launch.py']), # 복사할 파일
        ('share/color_seeker/urdf',
            ['urdf/robot.urdf']),
        ('share/color_seeker/worlds',
            ['worlds/world.sdf', 'worlds/red_box.sdf', 'worlds/blue_box.sdf', 'worlds/green_box.sdf']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shy',
    maintainer_email='545austin@naver.com',
    description='Differential-drive robot in Gazebo that finds and approaches an object of a given color using its camera',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "color_seeker = color_seeker.color_seeker:main", # "실행이름 = 패키지.파일:main"
            "commander = color_seeker.commander:main"
        ],
    },
)
