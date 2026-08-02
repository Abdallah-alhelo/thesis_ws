import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # 1. Hardcode the AWS models path so Gazebo never fails to find the hospital props
    home_dir = os.environ['HOME']
    aws_models_path = os.path.join(home_dir, 'thesis_ws', 'src', 'aws-robomaker-hospital-world', 'models')
    
    set_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=[os.environ.get('GAZEBO_MODEL_PATH', ''), ':', aws_models_path]
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

    # 4. Start the Robot State Publisher for TurtleBot3
    tb3_rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch', 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )
    
    # 5. Spawn the TurtleBot3 Waffle Pi into the world
    tb3_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch', 'spawn_turtlebot3.launch.py')
        ),
        launch_arguments={
            'x_pose': '0.0',
            'y_pose': '0.0',
            'z_pose': '0.2' # Elevated slightly so the robot doesn't clip into the floor
        }.items()
    )

    return LaunchDescription([
        set_model_path,
        aws_hospital_launch,
        gzclient,
        tb3_rsp,
        tb3_spawn
    ])
