#!/usr/bin/env python3
import rospy
import math
from geometry_msgs.msg import Vector3Stamped

# 全域變數 
yaw_data = []

def imu_callback(msg):
    global yaw_data
    yaw_data.append(msg.vector.z)

def initiate():
    rospy.init_node('filter_stability_test', anonymous=True)
    rospy.Subscriber('/imu_filter/rpy/filtered', Vector3Stamped, imu_callback)
    
    rospy.loginfo("實車靜態穩定度測試啟動...")
    rospy.loginfo("【測試指示】請確保割草機處於完全靜止狀態，不要啟動馬達。")
    rospy.loginfo("數據採集中... 按 Ctrl+C 結束採集並輸出分析報告。")
    
    rospy.spin()

def calculate_rms():
    global yaw_data
    if len(yaw_data) == 0:
        print("\n[警告] 未收到任何實體感測器數據！請確認 ROS 節點是否正常運作。")
        return

    mean_yaw = sum(yaw_data) / len(yaw_data)
    variance = sum((x - mean_yaw) ** 2 for x in yaw_data) / len(yaw_data)
    rms = math.sqrt(variance)
    
    print("\n==============================")
    print("NEXMOW 實車靜態穩定度測試報告")
    print("==============================")
    print(f"有效數據點: {len(yaw_data)} 筆")
    print(f"平均航向角: {mean_yaw:.4f}")
    print(f"系統底噪 (RMS): {rms:.6f}")
    print("==============================")
    
    # 實車內部存檔路徑 
    log_path = '/home/pi3test/stability_result_real.txt'
    with open(log_path, 'w') as f:
        f.write("NEXMOW Static Stability Report\n")
        f.write("-" * 30 + "\n")
        f.write(f"Data Points: {len(yaw_data)}\n")
        f.write(f"Mean Yaw: {mean_yaw:.4f}\n")
        f.write(f"RMS Noise: {rms:.6f}\n")
    print(f"[系統提示] 分析報告已匯出至: {log_path}")

if __name__ == '__main__':
    try:
        initiate()
    except rospy.ROSInterruptException:
        pass
    finally:
        calculate_rms()