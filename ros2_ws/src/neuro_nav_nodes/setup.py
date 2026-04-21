from setuptools import setup, find_packages
package_name = 'neuro_nav_nodes'
setup(
    name=package_name,
    version='0.3.0',
    packages=find_packages(include=[package_name, f"{package_name}.*"]),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', ['config/controller.yaml']),
    ],
    install_requires=['setuptools', 'numpy'],
    zip_safe=True,
    maintainer='Faizan Ahmed Khan',
    maintainer_email='faizan@example.com',
    description='ROS 2 nodes for the Neuro-Embedded Navigation Lab.',
    license='MIT',
    entry_points={'console_scripts': [
        'sensor_fusion_node = neuro_nav_nodes.sensor_fusion_node:main',
        'neuro_controller_node = neuro_nav_nodes.neuro_controller_node:main',
        'mission_supervisor_node = neuro_nav_nodes.mission_supervisor_node:main',
        'experiment_logger_node = neuro_nav_nodes.experiment_logger_node:main',
    ]},
)
