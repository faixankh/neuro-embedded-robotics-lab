from setuptools import find_packages, setup
package_name = 'neuro_nav_experiments'
setup(
    name=package_name,
    version='0.2.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', ['config/experiment_matrix.yaml']),
        ('share/' + package_name + '/launch', ['launch/batch_eval.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Faizan Ahmed',
    maintainer_email='faizan@example.com',
    description='Experiment package for neuro navigation.',
    entry_points={'console_scripts': [
        'mission_metrics_aggregator = neuro_nav_experiments.mission_metrics_aggregator:main',
        'failure_taxonomy_logger = neuro_nav_experiments.failure_taxonomy_logger:main',
    ]},
)