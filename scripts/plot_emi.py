import pandas as pd
import matplotlib.pyplot as plt
import os

# 自動偵測檔案路徑 
# 優先找實車版檔案，找不到再找模擬版檔案
if os.path.exists('emi_log_auto.csv'):
    csv_filename = 'emi_log_auto.csv'
else:
    csv_filename = 'emi_log_auto_test.csv'

try:
    print(f"正在讀取資料: {csv_filename}...")
    df = pd.read_csv(csv_filename)
    
    # 使用 .values 將數據轉為 Numpy 陣列，解決索引報錯問題
    time_data = df['Time(s)'].values
    yaw_data = df['Yaw'].values
    
    # 建立畫布
    plt.figure(figsize=(12, 6))
    
    # 畫出 Yaw 數據線
    plt.plot(time_data, yaw_data, label='Yaw (Z-axis) Angle', color='b', linewidth=1.5)
    
    # 標示馬達啟動與關閉的區間 (5s - 20s) 
    # 用 try-except 包起來，避免數據長度不足時報錯
    if time_data.max() >= 5:
        plt.axvspan(0, 5, color='green', alpha=0.1, label='Motor OFF (Baseline)')
        plt.axvline(x=5, color='r', linestyle='--', linewidth=2)
        
        if time_data.max() >= 20:
            plt.axvspan(5, 20, color='red', alpha=0.1, label='Motor ON (Interference)')
            plt.axvline(x=20, color='r', linestyle='--', linewidth=2)
    
    # 設定圖表標題與標籤
    plt.title(f'NEXMOW EMI Test: {csv_filename}', fontsize=14, fontweight='bold')
    plt.xlabel('Time (seconds)', fontsize=12)
    plt.ylabel('Yaw Angle (degrees)', fontsize=12)
    
    # 顯示網格與圖例
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(loc='upper right')
    
    # 調整邊距並儲存圖片
    plt.tight_layout()
    output_img = 'emi_result_plot.png'
    plt.savefig(output_img, dpi=300)
    print(f" 圖表繪製成功！已儲存為 {output_img}")

except Exception as e:
    print(f" 發生錯誤: {e}")