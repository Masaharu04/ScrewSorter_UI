import customtkinter as ctk
import tkinter.messagebox as messagebox
from datetime import datetime
from PIL import Image
import threading
import queue
import time
from src.viewmodels import MainViewModel
from src.base.menteviews import MaintenanceView  
from src.ui.UnderButton.UnderButton import UnderButtonFrame
from src.ui.EarPop.EarPopup import ErrorPopup
from src.ui.stocker.stoker import create_stocker_frame  # 追加
from src.ui.dateTime.dateTime import update_time  # dateTime.pyのupdate_timeをインポート
from src.ui.InputAmount.InputAmount import InputAmountFrame  # InputAmount.pyのInputAmountFrameをインポート
from src.struct_command import *
from ..struct_command import *

structsize = [
0, 2, 2, 3, 2, 4, 4, 3, 2, 12, 3, 3, 3, 4, 5, 2, 3,
2, 5, 4, 2, 2, 2, 2, 2, 3, 2, 3
]

class SerialThread:
  def __init__(self, receive_data_queue):
    self.receive_data_queue = receive_data_queue
    #self.serial_test_data = ([0x15,0x0b,0x50],[0x15,0x0b,0x30])
    self.serial_test_data = ([0x15,0x0b,0x50],[0x15,0x0b,0x30])
    # 処理スレッドの開始
    self.thread = threading.Thread(target=self.SerialProcess)
    self.thread.daemon = True
    self.thread.start()
    
  def SerialProcess(self):
    i = 0
    while True:
      #シリアル受信処理
      try:
        # 集計結果をキューに送信
        serial_get_data = self.serial_test_data[i]
        
        self.receive_data_queue.put(serial_get_data)
          
      except Exception as e:
        self.receive_data_queue.put((-1, str(e)))
      finally:
        #self.receive_data_queue.put(('close_window', None))
        i += 1
        if i>len(self.serial_test_data)-1 :
          i=0
        time.sleep(0.5)
      #シリアル送信処理
      try:
        data = self.receive_data_queue.get_nowait()
       # print(data)          
      except queue.Empty:
        pass
      finally:
        time.sleep(0.5)

class MainView:
    def __init__(self, master):
        self.master = master
        self.viewmodel = MainViewModel()
        self.error_popup = ErrorPopup(master)
        self.error_popup.set_viewmodel(self.viewmodel)
        self.setup_ui()
        self.start_error_monitoring()

        # カーソルを非表示にする
        self.master.config(cursor="")

    def setup_ui(self):
        self.master.geometry('800x480')
        self.master.title("メイン画面")
        self.master.overrideredirect(True)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # メインフレーム
        main_frame = ctk.CTkFrame(self.master, fg_color="#2b2b2b")
        main_frame.pack(fill="both", expand=True)

        # 上部フレーム（時間と投入量と中間ストッカーの残量）
        top_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b")
        top_frame.pack(fill="x", padx=10, pady=(10, 0))

        # 左側フレーム（時間、日付、投入量）
        left_frame = ctk.CTkFrame(top_frame, fg_color="#2b2b2b")
        left_frame.pack(side="left")

        #シリアル通信テスト
        self.p = Protocol()
        self.receive_data_queue = queue.Queue()
        self.thread = SerialThread(self.receive_data_queue)
        #self.check_queue()

        # 時間表示
        self.time_label = ctk.CTkLabel(left_frame, text="10:55", font=("Arial", 60, "bold"), text_color="#ffffff")
        self.time_label.pack(anchor="center", pady=(0, 0))

        # 日付表示
        self.date_label = ctk.CTkLabel(left_frame, text="8月27日火曜日", font=("Arial", 18), text_color="#cccccc")
        self.date_label.pack(anchor="center", pady=(0, 5))

        #投入量の残量
        self.amount_label = self.create_amount_display(left_frame)  # 追加
        self.check_queue()

        # 中間ストッカーの残量
        create_stocker_frame(top_frame)  # 変更

        # 下部フレーム（ボタン）
        self.under_button = UnderButtonFrame(main_frame, self)



        self.update_time()

    #シリアル通信へのリクエスト
    def check_queue(self):
          try:
              data = self.receive_data_queue.get_nowait()
              self.p = self.p.set_protocol(data,structsize)

              self.stocker_capacity = self.p.inputStockerStatus.capacity
              self.update_amount_display(self.amount_label,self.stocker_capacity)
              print(self.p.inputStockerStatus)
          
              #self.midStockerStatus_capacity = self.p.midStockerStatus.capacity
              #print(self.p.midStockerStatus)
          except queue.Empty:
              pass
          finally:
              self.master.after(100, self.check_queue)


    def create_amount_display(self, parent_frame):
        # 投入量表示フレームを作成
        self.amount_label = ctk.CTkLabel(parent_frame, text="", font=("Arial", 28, "bold"), text_color="#3b8ed0")
        self.amount_label.pack(anchor="center", padx=35, pady=(15, 0))

        self.rate_label = ctk.CTkLabel(parent_frame, text="投入口の稼働率", font=("Arial", 12), text_color="#cccccc")
        self.rate_label.pack(anchor="center", padx=5, pady=(0, 5))
        input_amount = 10
        self.amount_label.configure(text=f"投入量 {input_amount}%")
        return self.amount_label
    
    def update_amount_display(self, amount_label, input_amount):
        amount_label.configure(text=f"投入量 {input_amount}%")  # ラベルを更新

    def update_time(self):
        update_time(self.time_label, self.date_label)  # dateTime.pyのupdate_timeを呼び出す

    def display_message(self, text):
        print(text)  # メッセージをコンソールに出力

    def show_warning(self):
        # テスト用にエラーコードをセット
        self.viewmodel.set_error_code("E001")

    def on_settings_close(self):
        self.master.deiconify()

    def open_maintenance_view(self):
        # メンテナンス画面を開く前に、元のウィンドウを隠す
        maintenance_window = ctk.CTkToplevel(self.master)
        MaintenanceView(maintenance_window, self.on_maintenance_close)
        self.master.withdraw()  # メンテナンス画面が開いた後に、元のウィンドウを隠す
        maintenance_window.protocol("WM_DELETE_WINDOW", self.on_maintenance_close)

    def on_maintenance_close(self):
        self.master.deiconify()

    def start_error_monitoring(self):
        # エラーコードをチェックして、必要に応じてポップアップを表示
        error_code = self.viewmodel.get_error_code()  # ViewModelからエラーコードを取得
        if error_code:
            self.error_popup.show_error(error_code)
        self.master.after(1000, self.start_error_monitoring)  # 1秒ごとにチェック

    def update_stocker_labels(self, selected_values):
        # 選択されたストッカーを表示する処理を追加
        print(f"表示するストッカー: {selected_values}")
        # ここでUIに反映させる処理を追加することができます

def start_main_view():
    root = ctk.CTk()
    main_view = MainView(root)
    root.mainloop()
