# NEXMOW Field Test Plan: EMI Analysis & EKF Tuning
**Location:** Shuiyuan Campus
**Objectives:** Quantify blade motor electromagnetic interference, measure pre-EKF baseline noise, and record ROS sensor data (Rosbag).

## Phase 1: Physical & Environment Setup
1. **Safe Jacking:** Use support blocks to elevate the mower. Ensure both the cutting blades and wheels are completely suspended.
2. **Communication Link:** Connect the laptop to the mower's network and verify communication with the ROS Master.
3. **Launch 🪟 Terminal A** and navigate to the workspace:
    ```bash
    wsl
    cd /mnt/c/Users/willy/Desktop/智慧車輛/EMU_test
    ```

## Phase 2: Static Baseline Test
**Objective:** Measure the natural sensor noise floor while the mower is completely stationary and the motor is OFF.

1. Ensure the mower is stationary and untouched.
2. In **🪟 Terminal A**, execute the stability test script:
    ```bash
    python3 src/filter_stability_test.py
    ```
3. **Record:** Note the `Yaw Mean` and `RMS` values printed in the terminal. This serves as the zero-interference baseline.

## Phase 3: Active EMI Test & Data Logging (Rosbag)
**Objective:** Activate the blade motor to induce EMI while simultaneously logging CSV data (for plotting) and a Bag file (for offline EKF tuning).

1. **Prepare Dual Terminals:** Open a new WSL window for ** Terminal B**, and navigate to the same directory:
    ```bash
    wsl
    cd /mnt/c/Users/willy/Desktop/智慧車輛/EMU_test
    ```
2. **Start Rosbag Recording (in Terminal A):** Enter the command and press Enter. The terminal will pause, indicating it is recording.
    ```bash
    rosbag record -O results/mower_emi_test_01 /imu/data /odom
    ```
3. **Trigger Automated Test Script (in Terminal B):** Execute the logger script to start the motor and record the CSV.
    ```bash
    python3 src/mag_interference_logger.py
    ```
    > ⚠️ **Note:** The script automatically runs the sequence: "Start -> Run for 15s -> Stop". Keep hands clear of the mower during execution.
4. **Stop Recording:** Once Terminal B indicates the test is complete, return to ** Terminal A** and press `Ctrl + C` to stop the rosbag recording.

## Phase 4: On-Site Data Validation
**Objective:** Verify that the data was successfully captured and exhibits clear EMI characteristics before disconnecting.

1. In either terminal, execute the plotting script:
    ```bash
    python3 scripts/plot_emi.py
    ```
2. **Verify Results:** Check the pop-up graph or the `emi_result_plot.png` generated in the `results/` folder. A successful test will show distinct waveform fluctuations during the "Active Region".