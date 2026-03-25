##!/usr/bin/env python3
import rospy
import csv
import time
from std_msgs.msg import Bool
from geometry_msgs.msg import Vector3Stamped

# --- 實車內部存檔路徑 ---
csv_file_path = '/home/pi3test/emi_log_auto.csv'
file = None
writer = None
start_time = 0
is_recording = False

def imu_callback(msg):
    global writer, start_time, is_recording
    # 只有在 is_recording 為 True 時才寫入資料
    if writer is not None and is_recording:
        current_time = time.time() - start_time
        writer.writerow([current_time, msg.vector.x, msg.vector.y, msg.vector.z])

# ==========================================
# 依據簡報加入的刀盤控制函式 
# ==========================================
def blade_on(blade_start_pub, rate):
    rospy.loginfo("開啟刀盤")
    blade_start_pub.publish(True)
    rate.sleep()

def blade_off(blade_start_pub):
    rospy.loginfo("關閉刀盤")
    blade_start_pub.publish(False)

# ==========================================
# 主流程
# ==========================================
def initiate():
    global file, writer, start_time, is_recording
    
    rospy.init_node('mag_interference_logger_auto', anonymous=True)
    rospy.Subscriber('/imu_filter/rpy/filtered', Vector3Stamped, imu_callback)
    
    # 建立刀盤控制連線
    blade_start_pub = rospy.Publisher('/base_node/blade_start', Bool, queue_size=1)
    
    rospy.sleep(1.0)
    rate = rospy.Rate(10)
    
    rospy.loginfo("等待實體刀盤連線中...")
    while blade_start_pub.get_num_connections() == 0:
        rospy.sleep(0.5)
        
    rospy.loginfo("已與刀盤建立連線")
    
    # 準備寫入 CSV
    file = open(csv_file_path, mode='w', newline='')
    writer = csv.writer(file)
    # 在標頭多加了一個欄位，讓之後看資料就知道這是什麼
    writer.writerow(['Time(s)', 'Roll', 'Pitch', 'Yaw']) 
    
    start_time = time.time()
    is_recording = True
    
    # --------------------------------------------------
    #  自動化測試劇本開始 (取代原本無限等待的 rospy.spin)
    # --------------------------------------------------
    rospy.loginfo(">>> 階段 1/3: 錄製靜止基準底噪 (5 秒)...")
    rospy.sleep(5.0)  # 讓程式等待 5 秒，這期間 callback 仍會持續背景寫入資料
    
    rospy.loginfo(">>> 階段 2/3: 啟動馬達！錄製運轉干擾 (15 秒)...")
    blade_on(blade_start_pub, rate)
    rospy.sleep(15.0) # 讓刀盤轉 15 秒
    
    rospy.loginfo(">>> 階段 3/3: 測試完畢，準備關閉...")
    blade_off(blade_start_pub)
    
    # 停止錄製
    is_recording = False
    rospy.sleep(1.0) # 給系統一點緩衝時間確實關閉刀盤

if __name__ == '__main__':
    try:
        initiate()
    except rospy.ROSInterruptException:
        pass
    finally:
        # 確保檔案安全關閉
        if file is not None and not file.closed:
            file.close()
            print(f"\n 自動 EMI 測試結束，檔案已儲存至 {csv_file_path}")