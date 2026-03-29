# ROS1 Soccer Bot Simulation

A two-robot autonomous and teleoperated soccer simulation built with ROS (Noetic), Gazebo, and OpenCV. Developed as a course project for M.Tech Robotics and Automation at the College of Engineering Trivandrum (2025).

![ROS](https://img.shields.io/badge/ROS-Noetic-blue) ![Gazebo](https://img.shields.io/badge/Simulator-Gazebo-orange) ![Python](https://img.shields.io/badge/Python-3.x-green)

---

## Overview

This project implements a fully simulated differential-drive robot capable of autonomously detecting, tracking, and pushing a soccer ball toward a goal using HSV-based computer vision. A second robot (red) supports simultaneous teleoperation, enabling two-player competitive gameplay entirely within simulation.

**Key features:**
- Custom URDF robot model with differential-drive kinematics and a forward-mounted camera
- 9 × 6 m textured Gazebo soccer field with walls, goalposts, and a dynamic ball
- HSV-based orange ball detection with morphological noise filtering and contour extraction
- Proportional control for approach, alignment, and ball-push behavior
- Search/recovery mode when ball is lost from frame
- Dual teleoperation: WASD (blue robot) + arrow keys (red robot) via pygame
- Namespace-isolated multi-robot ROS topic architecture
---

## System Architecture

```
Gazebo Simulation
      │
      ▼
/camera/image_raw  ──►  ball_follower.py  ──►  /cmd_vel_blue
                              │
                         HSV masking
                         Contour detection
                         Proportional control
                         Search/recovery logic

/cmd_vel_blue  ──►  diff_drive plugin  ──►  Blue robot motion
/cmd_vel_red   ──►  diff_drive plugin  ──►  Red robot motion
```

---

## Dependencies

- ROS Noetic (Ubuntu 20.04)
- Gazebo 11
- `rospy`, `cv_bridge`, `sensor_msgs`, `geometry_msgs`
- OpenCV (`cv2`)
- pygame (for dual teleoperation)

Install Python dependencies:
```bash
pip install pygame opencv-python
```

Install ROS dependencies:
```bash
rosdep install --from-paths src --ignore-src -r -y
```

---

## Running the Simulation

**1. Build the workspace:**
```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

**2. Launch the full simulation:**
```bash
roslaunch ros1_soccerbot soccer_sim.launch
```

**3. Start autonomous ball-following (blue robot):**
```bash
rosrun ros1_soccerbot ball_follower.py
```

**4. Start dual teleoperation:**
```bash
rosrun ros1_soccerbot teleop_blue.py   # WASD keys
rosrun ros1_soccerbot teleop_red.py    # Arrow keys
```

---

## Robot Design

| Parameter | Value |
|---|---|
| Chassis | 20 cm × 15 cm × 40 cm |
| Wheel radius | 5.5 cm |
| Wheel separation | 24 cm |
| Camera FOV | ~57° horizontal |
| Camera resolution | 640 × 480 @ 30 fps |
| Drive | Differential drive (gazebo_ros_diff_drive) |

---

## Vision Pipeline

1. Subscribe to `/camera/image_raw`
2. Convert BGR → HSV
3. Apply HSV mask for orange ball detection
4. Morphological open/close to remove noise
5. Find contours → compute centroid and radius
6. Generate `cmd_vel` based on horizontal error (proportional control)
7. If ball lost → enter search mode (rotate + reverse)

---

## Results

The system successfully demonstrated:
- Reliable ball detection and tracking under varied field textures
- Smooth approach and push behavior toward the goal
- Stable multi-robot operation with isolated ROS namespaces
- Responsive dual teleoperation via keyboard

---

## Future Work

- PID controller for smoother tracking
- LiDAR integration for depth-aware navigation
- SLAM-based field mapping
- Multi-robot cooperation strategies
- Reinforcement learning-based agent

---

## Author

**Adil Naz Muhammed**  
M.Tech Robotics and Automation, College of Engineering Trivandrum  
[LinkedIn](https://www.linkedin.com/in/adil-naz-muhammed) | [Email](mailto:adilnazmuhammed.mec@gmail.com)

---

## Acknowledgements

Course project submitted to APJ Abdul Kalam Technological University under the guidance of Prof. Joaquim Ignatious Monteiro, Prof. Shafeek M, and Prof. Merlin Mon Mathew.
