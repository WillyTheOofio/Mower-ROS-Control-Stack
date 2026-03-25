This is my development workspace for the NEXMOW robotic mower. It’s where I’m building the "brain" to make the machine smarter and more precise.

# Why this project? 🤌🤌
I am a Mechanical Engineering student at NTU. Before this, my world was mostly about CAD, thermodynamics, and physical structures. I had zero experience with ROS, Python-based remote control, or sensor fusion. But I noticed a problem: the mower was "going crooked", the trajectory was ass. I realized that no amount of mechanical tweaking could fix it, I had to learn the software side. This repo is a record of me learning robotics from scratch to solve real-world hardware headaches.
## Current Focus: Fixing the slip 👌
Right now, I’m tackling the most frustrating part: Heading Stabilization.

The Issue: When the mower’s massive blades start spinning, they create huge Electromagnetic Interference (EMI). This makes the magnetometer (compass) go crazy, causing the mower to drift off-course.

What I’ve built: I developed a custom automated logger to map out exactly how the motor noise affects the sensors.

The Goal: Use IMU data to compensate for that noise so the mower can actually drive in a straight line on the grass.

## What’s Next 🤞

Once I get the steering stable, I’m moving on to things that currently feel like a hard thing to do to me:

Ultrasonic Avoidance: Wiring up the sensor arrays so the mower stops hitting things and starts dodging them.

Vision-Based Autonomy: I want to use the onboard cameras to "see" where the grass ends. Since I haven't taken formal CS classes on this, I’m teaching myself OpenCV and basic perception logic as I go.

### Development Log 🗓️

#### **Update 1: System Analysis & Protocol Definition**
- **Analysis:** Conducted a deep dive into the NEXMOW codebase to map out ROS node communications.
- **Standardization:** Defined rigorous testing protocols for sensor stability and experimental data collection.
- **Data Integrity:** Corrected historical experimental data inconsistencies to establish a reliable baseline for performance tracking.

#### **Update 2: Automated EMI Diagnostic Suite**
- **Automation:** Developed `mag_interference_logger.py`, a script that automates the blade motor cycle (Start -> 15s Run -> Stop) to eliminate manual timing errors.
- **Simulation:** Successfully built and validated a "Virtual Mower" environment in WSL to verify ROS logic before field testing.
- **Visualization:** Integrated a Python-based data visualization tool (`plot_emi.py`) to generate high-resolution analysis reports immediately after each test run.
