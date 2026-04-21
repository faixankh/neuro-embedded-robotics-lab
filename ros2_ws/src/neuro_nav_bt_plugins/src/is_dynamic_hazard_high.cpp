#include <string>
// Skeleton plugin for repository completeness; runtime implementation belongs in a ROS 2 build environment.
// Checks fused hazard score and returns SUCCESS when dynamic risk exceeds threshold.
namespace neuro_nav_bt_plugins {
struct IsDynamicHazardHigh {
  std::string description() const { return "Checks fused hazard score and returns SUCCESS when dynamic risk exceeds threshold."; }
};
}