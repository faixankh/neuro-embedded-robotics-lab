#include <string>
// Skeleton plugin for repository completeness; runtime implementation belongs in a ROS 2 build environment.
// Requests neuro takeover via service and writes mode to BT blackboard.
namespace neuro_nav_bt_plugins {
struct SwitchToNeuroController {
  std::string description() const { return "Requests neuro takeover via service and writes mode to BT blackboard."; }
};
}