Send a waypoint for the `ego_planner` with:
```bash
ros2 topic pub --once /goal_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'map'},
  pose: {
    position: {x: 4.0, y: 4.0, z: 3.0},
    orientation: {w: 1.0}
  }
}"
```
