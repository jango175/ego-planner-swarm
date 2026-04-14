#include <Eigen/Eigen>
#include "quadrotor_msgs/msg/position_command.hpp"
#include <rclcpp/rclcpp.hpp>
#include <rclcpp/timer.hpp>
#include <chrono>
#include <limits>
#include <iostream>

using namespace std::chrono_literals;

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);

  // 创建节点
  auto node = rclcpp::Node::make_shared("quad_sim_example");

  // 创建发布者
  auto cmd_pub = node->create_publisher<quadrotor_msgs::msg::PositionCommand>("/position_cmd", 10);

  // 延迟2秒钟
  rclcpp::sleep_for(2s);

  std::chrono::milliseconds period_ms(10);
  int tick_count = 0;

  rclcpp::TimerBase::SharedPtr pub_timer_ = node->create_wall_timer(
    period_ms,
    [&]()
    {
      tick_count++;

      auto cmd = quadrotor_msgs::msg::PositionCommand();

      if (tick_count <= 500)
      {
        if (tick_count == 1) {
          RCLCPP_INFO(node->get_logger(), "\033[42mPosition Control to (2,0,1) meters\033[0m");
        }
        cmd.position.x = 2.0;
        cmd.position.y = 0.0;
        cmd.position.z = 1.0;
        cmd_pub->publish(cmd);
      }
      else if (tick_count > 500 && tick_count <= 1000)
      {
        if (tick_count == 501)
        {
          RCLCPP_INFO(node->get_logger(), "\033[42mVelocity Control to (-1,0,0) meters/second\033[0m");
        }
        cmd.position.x = std::numeric_limits<float>::quiet_NaN();
        cmd.position.y = std::numeric_limits<float>::quiet_NaN();
        cmd.position.z = std::numeric_limits<float>::quiet_NaN();
        cmd.velocity.x = -1.0;
        cmd.velocity.y = 0.0;
        cmd.velocity.z = 0.0;
        cmd_pub->publish(cmd);
      }
      else if (tick_count > 1000 && tick_count <= 1500)
      {
        if (tick_count == 1001)
        {
          RCLCPP_INFO(node->get_logger(), "\033[42mAcceleration Control to (1,0,0) meters/second^2\033[0m");
        }
        cmd.position.x = std::numeric_limits<float>::quiet_NaN();
        cmd.position.y = std::numeric_limits<float>::quiet_NaN();
        cmd.position.z = std::numeric_limits<float>::quiet_NaN();
        cmd.velocity.x = std::numeric_limits<float>::quiet_NaN();
        cmd.velocity.y = std::numeric_limits<float>::quiet_NaN();
        cmd.velocity.z = std::numeric_limits<float>::quiet_NaN();
        cmd.acceleration.x = 1.0;
        cmd.acceleration.y = 0.0;
        cmd.acceleration.z = 0.0;
        cmd_pub->publish(cmd);
      }
      else
      {
        tick_count = 0; 
      }
    }
  );

  rclcpp::spin(node);

  rclcpp::shutdown();
  return 0;
}