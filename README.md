# Changes in this fork
* Added support for ROS 2 Jazzy.
* Package now work with 2D LIDAR data.
* Added look-around spin in the beginning of the trajectory.

# Usage
## 1. Required Libraries 
* vtk (A dependency library for PCL installation, need to check Qt during compilation)
* PCL

## 2. Prerequisites
It might be due to some incorrect settings in my publish/subscribe configurations. Using ROS2's default FastDDS causes significant lag during program execution. The reason hasn't been identified yet. Please follow the steps below to change the DDS to cyclonedds.

### 2.1 Install cyclonedds
```bash
sudo apt install ros-humble-rmw-cyclonedds-cpp
```

### 2.2 Change default DDS
```bash
echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc
source ~/.bashrc
```

### 2.3 Verify the change
```bash
ros2 doctor --report | grep "RMW middleware"
```
If the output shows `rmw_cyclonedds_cpp`, the modification is successful.

## 3. Running the Code
### 3.1 Launch Rviz
```bash
ros2 launch ego_planner rviz.launch.py
```
### 3.2 Run the planning program
Open a new terminal and execute:
* Single drone
```bash
ros2 launch ego_planner single_run_in_sim.launch.py
```
* swarm
```bash
ros2 launch ego_planner swarm.launch.py
```
* large swarm
```bash
ros2 launch ego_planner swarm_large.launch.py
```
* Additional parameters (optional):
    * `use_mockamap`: Map generation method. Default: False (uses Random Forest), True uses mockamap.
    * `use_dynamic`: Whether to consider dynamics. Default: False (disabled), True enables dynamics.
```bash
ros2 launch ego_planner single_run_in_sim.launch.py use_mockamap:=True use_dynamic:=False
```

# Sources
* https://github.com/ZJU-FAST-Lab/ego-planner-swarm
* https://github.com/jango175/lidar_mapper
