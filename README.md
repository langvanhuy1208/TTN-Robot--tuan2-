# TTN-Robot--tuan2
# terminal 1 chay rviz
ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur3 launch_rviz:=true

# terminal 2 
# di chuyen vao thu muc
cd ~/assignments_2_ws

# Build package assignments_2
colcon build --packages-select assignments_2

# nap moi truong
source install/setup.bash

# chay node thuc thi
ros2 run assignments_2 skill_executor_node
