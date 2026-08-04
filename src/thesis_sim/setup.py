import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'thesis_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # ADD THIS LINE TO INSTALL LAUNCH FILES:
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='AbdAllahAlhelo',
    maintainer_email='abdallah.alhelo@study.thws.de',
    description='launch the simulation starting state',
    license='Abd',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
