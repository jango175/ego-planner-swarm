from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # LaunchConfigurations
    map_size_x = LaunchConfiguration('map_size_x_', default=45.0)
    map_size_y = LaunchConfiguration('map_size_y_', default=45.0)
    map_size_z = LaunchConfiguration('map_size_z_', default=30.0)

    odometry_topic = LaunchConfiguration('odometry_topic', default='odom')
    camera_pose_topic = LaunchConfiguration('camera_pose_topic', default='camera_pose')
    depth_topic = LaunchConfiguration('depth_topic', default='depth_image')
    cloud_topic = LaunchConfiguration('cloud_topic', default='cloud')

    cx = LaunchConfiguration('cx', default=321.04638671875)
    cy = LaunchConfiguration('cy', default=243.44969177246094)
    fx = LaunchConfiguration('fx', default=387.229248046875)
    fy = LaunchConfiguration('fy', default=387.229248046875)

    max_vel = LaunchConfiguration('max_vel', default=2.0)
    max_acc = LaunchConfiguration('max_acc', default=1.0)
    planning_horizon = LaunchConfiguration('planning_horizon', default=12.0)

    # Waypoints (only used if flight_type == 2)
    point_num = LaunchConfiguration('point_num', default=1)
    point0_x = LaunchConfiguration('point0_x', default=0.0)
    point0_y = LaunchConfiguration('point0_y', default=0.0)
    point0_z = LaunchConfiguration('point0_z', default=0.0)

    flight_type = LaunchConfiguration('flight_type', default=1) # 1 = RViz Goal, 2 = Waypoints
    use_distinctive_trajs = LaunchConfiguration('use_distinctive_trajs', default=True)

    obj_num_set = LaunchConfiguration('obj_num_set', default=10)

    drone_id = LaunchConfiguration('drone_id', default=0)

    use_sim_time = LaunchConfiguration("use_sim_time", default=True)

    # DeclareLaunchArguments
    map_size_x_arg = DeclareLaunchArgument('map_size_x_', default_value=map_size_x, description='Map size along X')
    map_size_y_arg = DeclareLaunchArgument('map_size_y_', default_value=map_size_y, description='Map size along Y')
    map_size_z_arg = DeclareLaunchArgument('map_size_z_', default_value=map_size_z, description='Map size along Z')
    odometry_topic_arg = DeclareLaunchArgument('odometry_topic', default_value=odometry_topic, description='Odometry topic')
    camera_pose_topic_arg = DeclareLaunchArgument('camera_pose_topic', default_value=camera_pose_topic, description='Camera pose topic')
    depth_topic_arg = DeclareLaunchArgument('depth_topic', default_value=depth_topic, description='Depth topic')
    cloud_topic_arg = DeclareLaunchArgument('cloud_topic', default_value=cloud_topic, description='Point cloud topic')
    cx_arg = DeclareLaunchArgument('cx', default_value=cx, description='Camera intrinsic cx')
    cy_arg = DeclareLaunchArgument('cy', default_value=cy, description='Camera intrinsic cy')
    fx_arg = DeclareLaunchArgument('fx', default_value=fx, description='Camera intrinsic fx')
    fy_arg = DeclareLaunchArgument('fy', default_value=fy, description='Camera intrinsic fy')
    max_vel_arg = DeclareLaunchArgument('max_vel', default_value=max_vel, description='Maximum velocity')
    max_acc_arg = DeclareLaunchArgument('max_acc', default_value=max_acc, description='Maximum acceleration')
    planning_horizon_arg = DeclareLaunchArgument('planning_horizon', default_value=planning_horizon, description='Planning horizon')

    point_num_arg = DeclareLaunchArgument('point_num', default_value=point_num, description='Number of waypoints')
    point0_x_arg = DeclareLaunchArgument('point0_x', default_value=point0_x, description='Waypoint 0 X coordinate')
    point0_y_arg = DeclareLaunchArgument('point0_y', default_value=point0_y, description='Waypoint 0 Y coordinate')
    point0_z_arg = DeclareLaunchArgument('point0_z', default_value=point0_z, description='Waypoint 0 Z coordinate')

    flight_type_arg = DeclareLaunchArgument('flight_type', default_value=flight_type, description='flight_type')
    use_distinctive_trajs_arg = DeclareLaunchArgument('use_distinctive_trajs', default_value=use_distinctive_trajs, description='Use distinctive trajectories')
    obj_num_set_arg = DeclareLaunchArgument('obj_num_set', default_value=obj_num_set, description='Number of objects')
    drone_id_arg = DeclareLaunchArgument('drone_id', default_value=drone_id, description='Drone ID')

    # EGO planner node
    ego_planner_node = Node(
        package='ego_planner',
        executable='ego_planner_node',
        name=['drone_', drone_id, '_ego_planner_node'],
        output='screen',
        remappings=[
            ('odom_world', ['drone_', drone_id, '_', odometry_topic]),
            ('planning/bspline', ['drone_', drone_id, '_planning/bspline']),
            ('planning/data_display', ['drone_', drone_id, '_planning/data_display']),
            ('planning/broadcast_bspline_from_planner', '/broadcast_bspline'),
            ('planning/broadcast_bspline_to_planner', '/broadcast_bspline'),

            ('goal_point', ['drone_', drone_id, '_plan_vis/goal_point']),
            ('global_list', ['drone_', drone_id, '_plan_vis/global_list']),
            ('init_list', ['drone_', drone_id, '_plan_vis/init_list']),
            ('optimal_list', ['drone_', drone_id, '_plan_vis/optimal_list']),
            ('a_star_list', ['drone_', drone_id, '_plan_vis/a_star_list']),

            ('grid_map/odom', ['drone_', drone_id, '_', odometry_topic]),
            ('grid_map/cloud', ['drone_', drone_id, '_', cloud_topic]),
            ('grid_map/pose', ['drone_', drone_id, '_', camera_pose_topic]),
            ('grid_map/depth', ['drone_', drone_id, '_', depth_topic]),
            ('grid_map/occupancy_inflate', ['drone_', drone_id, '_grid/grid_map/occupancy_inflate']),

            ('/move_base_simple/goal', '/goal_pose'),
            ('position_cmd', '/planning/pos_cmd')
        ],
        parameters=[{
            'use_sim_time': use_sim_time,

            'fsm/flight_type': flight_type,
            'fsm/thresh_replan_time': 1.0,
            'fsm/thresh_no_replan_meter': 1.0,
            'fsm/planning_horizon': planning_horizon,
            'fsm/planning_horizen_time': 3.0,
            'fsm/emergency_time': 1.0,
            'fsm/realworld_experiment': False,
            'fsm/fail_safe': True,
            'fsm/do_init_spin': True,

            'fsm/waypoint_num': point_num,
            'fsm/waypoint0_x': point0_x,
            'fsm/waypoint0_y': point0_y,
            'fsm/waypoint0_z': point0_z,

            'grid_map/resolution': 0.1,
            'grid_map/map_size_x': map_size_x,
            'grid_map/map_size_y': map_size_y,
            'grid_map/map_size_z': map_size_z,
            'grid_map/local_update_range_x': 8.5,
            'grid_map/local_update_range_y': 8.5,
            'grid_map/local_update_range_z': 7.5,
            'grid_map/obstacles_inflation': 1.5,
            'grid_map/local_map_margin': 20,
            'grid_map/ground_height': -0.5,

            # Camera parameter
            'grid_map/cx': cx,
            'grid_map/cy': cy,
            'grid_map/fx': fx,
            'grid_map/fy': fy,

            # Depth filter
            'grid_map/use_depth_filter': False,
            'grid_map/depth_filter_tolerance': 0.15,
            'grid_map/depth_filter_maxdist': 5.0,
            'grid_map/depth_filter_mindist': 0.2,
            'grid_map/depth_filter_margin': 2,
            'grid_map/k_depth_scaling_factor': 1000.0,
            'grid_map/skip_pixel': 2,

            # Local fusion
            'grid_map/p_hit': 0.65,
            'grid_map/p_miss': 0.35,
            'grid_map/p_min': 0.12,
            'grid_map/p_max': 0.90,
            'grid_map/p_occ': 0.80,
            'grid_map/min_ray_length': 0.03,
            'grid_map/max_ray_length': 12.0,

            'grid_map/virtual_ceil_height': 28.0,
            'grid_map/visualization_truncate_height': 30.0,
            'grid_map/show_occ_time': False,
            'grid_map/pose_type': 1,
            'grid_map/frame_id': 'map',

            # Planner manager
            'manager/max_vel': max_vel,
            'manager/max_acc': max_acc,
            'manager/max_jerk': 4.0,
            'manager/control_points_distance': 0.4,
            'manager/feasibility_tolerance': 0.05,
            'manager/planning_horizon': planning_horizon,
            'manager/use_distinctive_trajs': use_distinctive_trajs,
            'manager/drone_id': drone_id,

            # Trajectory optimization parameters
            'optimization/lambda_smooth': 1.0,
            'optimization/lambda_collision': 0.5,
            'optimization/lambda_feasibility': 0.1,
            'optimization/lambda_fitness': 1.0,
            'optimization/dist0': 1.5,
            'optimization/swarm_clearance': 0.5,
            'optimization/max_vel': max_vel,
            'optimization/max_acc': max_acc,

            # B-Spline parameters
            'bspline/limit_vel': max_vel,
            'bspline/limit_acc': max_acc,
            'bspline/limit_ratio': 1.1,

            # Object prediction parameters
            'prediction/obj_num': obj_num_set,
            'prediction/lambda': 1.0,
            'prediction/predict_rate': 1.0
        }]
    )

    # Trajectory server node
    traj_server_node = Node(
        package='ego_planner',
        executable='traj_server',
        name=['drone_', drone_id, '_traj_server'],
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'traj_server/time_forward': 1.0
        }],
        remappings=[
            ('planning/bspline', ['drone_', drone_id, '_planning/bspline']),
            ('position_cmd', '/planning/pos_cmd')
        ]
    )

    ldlidar_qos_bridge_node = Node(
        package='ego_planner',
        executable='ldlidar_qos_bridge.py',
        name='ldlidar_qos_bridge',
        output='screen',
        emulate_tty=True
    )

    # Create LaunchDescription
    ld = LaunchDescription()

    # Add LaunchArguments
    ld.add_action(map_size_x_arg)
    ld.add_action(map_size_y_arg)
    ld.add_action(map_size_z_arg)
    ld.add_action(odometry_topic_arg)
    ld.add_action(camera_pose_topic_arg)
    ld.add_action(depth_topic_arg)
    ld.add_action(cloud_topic_arg)
    ld.add_action(cx_arg)
    ld.add_action(cy_arg)
    ld.add_action(fx_arg)
    ld.add_action(fy_arg)
    ld.add_action(max_vel_arg)
    ld.add_action(max_acc_arg)
    ld.add_action(planning_horizon_arg)

    ld.add_action(point_num_arg)
    ld.add_action(point0_x_arg)
    ld.add_action(point0_y_arg)
    ld.add_action(point0_z_arg)

    ld.add_action(flight_type_arg)
    ld.add_action(use_distinctive_trajs_arg)
    ld.add_action(obj_num_set_arg)
    ld.add_action(drone_id_arg)

    ld.add_action(ego_planner_node)
    ld.add_action(traj_server_node)
    ld.add_action(ldlidar_qos_bridge_node)

    return ld
