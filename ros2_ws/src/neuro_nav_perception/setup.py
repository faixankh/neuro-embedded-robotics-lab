from setuptools import find_packages, setup
package_name = 'neuro_nav_perception'
setup(
    name=package_name,
    version='0.2.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', ['config/perception.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Faizan Ahmed',
    maintainer_email='faizan@example.com',
    description='Perception and sensor-health package for neuro navigation.',
    entry_points={'console_scripts': [
        'sensor_health_monitor = neuro_nav_perception.sensor_health_monitor:main',
        'degradation_injector = neuro_nav_perception.degradation_injector:main',
        'traversability_estimator = neuro_nav_perception.traversability_estimator:main',
    ]},
)