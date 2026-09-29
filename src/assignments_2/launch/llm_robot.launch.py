from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='assignments_2',
            executable='skill_executor_node',
            name='skill_executor_node',
            output='screen',
            parameters=[{'student_id': '23020745'}]
        )
    ])
