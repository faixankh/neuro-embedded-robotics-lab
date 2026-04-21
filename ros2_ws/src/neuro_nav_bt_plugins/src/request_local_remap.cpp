#include <string>
// Skeleton plugin for repository completeness; runtime implementation belongs in a ROS 2 build environment.
// Triggers local remap request when planner validity collapses in clutter.
namespace neuro_nav_bt_plugins {
struct RequestLocalRemap {
  std::string description() const { return "Triggers local remap request when planner validity collapses in clutter."; }
};
}