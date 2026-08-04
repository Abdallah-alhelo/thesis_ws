import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Combine BOTH explicit model paths so nothing is invisible!
    home_dir = os.environ['HOME']
    aws_models_path = os.path.join(home_dir, 'thesis_ws', 'src', 'aws-robomaker-hospital-world', 'models')
    tb3_models_path = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'models')
    
    combined_model_paths = os.environ.get('GAZEBO_MODEL_PATH', '') + ':' + aws_models_path + ':' + tb3_models_path
    
    set_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=combined_model_paths
    )

    set_tb3_model = SetEnvironmentVariable(
        name='TURTLEBOT3_MODEL',
        value='waffle_pi'
    )

    # 2. Launch the AWS Hospital World (gzserver)
    aws_hospital_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('aws_robomaker_hospital_world'), 'launch', 'hospital.launch.py')
        )
    )

    # 3. Force Launch Gazebo GUI (gzclient)
    gzclient = ExecuteProcess(
        cmd=['gzclient'],
        output='screen'
    )

    # 4. Start the Robot State Publisher for TurtleBot3 (Needed for RViz)
    tb3_rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch', 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )
    
    # 5. Spawn the TurtleBot3 directly from the SDF
    tb3_model_sdf_path = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'models',
        'turtlebot3_waffle_pi',
        'model.sdf'
    )

    tb3_spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'waffle_pi',
            '-file', tb3_model_sdf_path,
            '-x', '0.0',
            '-y', '19.0',
            '-z', '1.0', # Bumped to 1.0 to guarantee a safe drop above the floor
            '-Y', '1.6'
        ],
        output='screen',
    )

    return LaunchDescription([
        set_model_path,
        set_tb3_model,
        aws_hospital_launch,
        gzclient,
        tb3_rsp,
        tb3_spawn
    ])
