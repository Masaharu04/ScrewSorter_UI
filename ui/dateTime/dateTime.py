from datetime import datetime  # datetimeをインポート
import customtkinter as ctk  # customtkinterをインポート

def update_time(time_label, date_label):
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%m月%d日(%a)").replace("Mon", "月").replace("Tue", "火").replace("Wed", "水").replace("Thu", "").replace("Fri", "金").replace("Sat", "土").replace("Sun", "日")
    time_label.configure(text=f"{current_time}")
    date_label.configure(text=f"{current_date}")
    # 1秒ごとにこの関数を再呼び出しするための設定
    time_label.master.after(1000, update_time, time_label, date_label)  # time_label.masterを使用して再帰的に呼び出す
