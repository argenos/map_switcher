cmake_minimum_required(VERSION 2.8.3)
project(map_switcher)

find_package(catkin REQUIRED COMPONENTS
    rospy
    std_msgs
    geometry_msgs
    genmsg
    message_generation
    )

catkin_python_setup()

################################################
## Declare ROS messages, services and actions ##
################################################

## Generate services in the 'srv' folder
add_service_files(
  FILES
  SwitchMap.srv
)

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS
  std_msgs
  geometry_msgs
  message_runtime
)
include_directories(
)

install(PROGRAMS
  scripts/map_switcher
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}/scripts
)

