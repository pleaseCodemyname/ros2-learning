from setuptools import find_packages, setup

package_name = 'review2_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/review2_pkg/launch',
            ['launch/chit_chat_launch.py'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shy',
    maintainer_email='545austin@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "talker=review2_pkg.talker:main",
            "listener=review2_pkg.listener:main"
        ],
    },
)
