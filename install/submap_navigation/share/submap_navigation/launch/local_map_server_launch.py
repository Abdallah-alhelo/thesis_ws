import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    

    initial_submap = '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_3.yaml'

    return LaunchDescription([
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='local_submap_server',
            output='screen',
            parameters=[{
                'yaml_filename': initial_submap,
                'topic_name': 'submap',  # Broadcasts to /submap instead of /map
                'frame_id': 'map'        # Keeps it aligned with the global coordinate frame
            }]
        ),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_local_map',
            output='screen',
            parameters=[{
                'autostart': True,
                'node_names': ['local_submap_server']
            }]
        )
    ])
