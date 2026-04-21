#include <string>
// Skeleton plugin for repository completeness; runtime implementation belongs in a ROS 2 build environment.
// Fails mission branch when elapsed mission wall time exceeds the configured budget.
namespace neuro_nav_bt_plugins {
struct MissionTimeoutExceeded {
  std::string description() const { return "Fails mission branch when elapsed mission wall time exceeds the configured budget."; }
};
}