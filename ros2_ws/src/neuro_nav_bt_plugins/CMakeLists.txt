cmake_minimum_required(VERSION 3.8)
project(neuro_nav_bt_plugins)
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(behaviortree_cpp REQUIRED)
find_package(nav2_behavior_tree REQUIRED)
find_package(std_msgs REQUIRED)
find_package(neuro_nav_msgs REQUIRED)
add_library(${PROJECT_NAME} SHARED
  src/is_dynamic_hazard_high.cpp
  src/switch_to_neuro_controller.cpp
  src/request_local_remap.cpp
  src/mission_timeout_exceeded.cpp
)
ament_target_dependencies(${PROJECT_NAME}
  rclcpp behaviortree_cpp nav2_behavior_tree std_msgs neuro_nav_msgs
)
install(TARGETS ${PROJECT_NAME} DESTINATION lib)
install(DIRECTORY include/ DESTINATION include)
ament_package()