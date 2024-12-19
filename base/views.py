import customtkinter as ctk
import tkinter.messagebox as messagebox
from datetime import datetime
from PIL import Image
import threading
import queue
import time
import serial
from src.viewmodels import MainViewModel
from src.base.menteviews import MaintenanceView  
from src.ui.UnderButton.UnderButton import UnderButtonFrame
from src.ui.EarPop.EarPopup import ErrorPopup
from ..ui.stocker.stoker import StockerApp
from src.ui.dateTime.dateTime import update_time  # dateTime.pyのupdate_timeをインポート
from src.ui.InputAmount.InputAmount import InputAmountFrame  # InputAmount.pyのInputAmountFrameをインポート
from src.struct_command import *
from ..struct_command import *

SERIAL_PORT = '/dev/ttyS0'
BAUD_RATE = 115200

INPUT_ADDR = 1
DISCRIMINATION_ADDR = 2
RETURN_ADDR = 3
ALIGNMENT_ADDR = 4
MASTER_ADDR = 6 

structsize = [
0, 2, 2, 3, 2, 4, 4, 3, 2, 12, 3, 3, 3, 4, 5, 2, 3,
2, 5, 4, 2, 2, 2, 2, 2, 3, 2, 3
]

class SerialThread:
  def __init__(self, receive_data_queue,send_data_queue):
    self.receive_data_queue = receive_data_queue
    self.send_data_queue = send_data_queue

    self.serial_test_data = ([0x15,0x0b,0x50],[0x15,0x0b,0x30])

    try:
      self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except serial.SerialException as e:
      print(f"シリアルポートの初期化に失敗しました: {e}")
      self.ser = None

    # 処理スレッドの開始
    self.thread = threading.Thread(target=self.SerialProcess)
    self.thread.daemon = True
    self.thread.start()
    
  def SerialProcess(self):
    i = 0
    while True:
      serial_get_data = 0
      try:
        print(f"受信データ数: {self.ser.in_waiting}")
        print(getSelectBitValue(100,2))

        if self.ser.in_waiting >= 2:
          header:bytes = self.ser.read(2) #self.ser.readline()
          print(type(header))
          print({header.hex("-")})
          command_num:int = header[1]
          print("command_num hex")
          print(hex(command_num))
          print("command_num")
          print(command_num)
          data_size = structsize[command_num]
          print(type(int(data_size)))
          print(int(data_size))

          if self.ser.in_waiting >= data_size - 2:
            data:bytes = self.ser.read(data_size)
            print("残りのdata")
            print(data.hex("-"))
          else:
            data = 0
            print("only 2 data")

          serial_get_data = header + data
          print(serial_get_data.hex("-"))
          self.receive_data_queue.put(serial_get_data) 
        else:
          print("no data")
            
      except Exception as e:
        self.receive_data_queue.put((-1, str(e)))
      finally:
        i += 1
        if i>len(self.serial_test_data)-1 :
          i=0
        time.sleep(0.5)

      try:
          data_to_send = self.send_data_queue.get_nowait()
          self.ser.write(f"{data_to_send}\n".encode('utf-8'))
          print(f"Sent: {data_to_send}")
      except queue.Empty:
          pass
      finally:
          time.sleep(0.5)

def decimalToBinaryList(num: int):
    binary_representation = bin(num)[2:]
    bit_list = [int(bit) for bit in binary_representation.zfill(8)]
    return bit_list

def getSelectBitValue(num: int, bit_position: int):
    bit_list = decimalToBinaryList(num)
    bit_count = len(bit_list)

    if bit_position >= 0 and bit_position < bit_count:
      select_bit_value = bit_list[-(bit_position + 1)]
    else:
      print("error!")

    return select_bit_value

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
        #キューの初期化
        self.receive_data_queue = queue.Queue()
        self.send_data_queue = queue.Queue()
        self.thread = SerialThread(self.receive_data_queue, self.send_data_queue)

        # 時間表示
        self.time_label = ctk.CTkLabel(left_frame, text="10:55", font=("Arial", 60, "bold"), text_color="#ffffff")
        self.time_label.pack(anchor="center", pady=(0, 0))

        # 日付表示
        self.date_label = ctk.CTkLabel(left_frame, text="8月27日火曜日", font=("Arial", 18), text_color="#cccccc")
        self.date_label.pack(anchor="center", pady=(0, 5))

        #投入量の残量
        self.amount_label = self.create_amount_display(left_frame) 
        
        self.check_queue()

        # 中間ストッカーの残量
        self.update_stocker_value(top_frame)

        # 下部フレーム（ボタン）
        self.under_button = UnderButtonFrame(main_frame, self, self.stocker_frame.set_data)

        self.update_time()

    #シリアル通信へのリクエスト
    def check_queue(self):
          try:
            while True:
              data = self.receive_data_queue.get_nowait()
              self.p = self.p.set_protocol(data,structsize)
              command = data[1]

              if command == INPUTSTOCKERSTATUS:
                self.stocker_capacity = self.p.inputStockerStatus.capacity
                self.update_amount_display(self.amount_label,self.stocker_capacity)

          except queue.Empty:
              pass
          finally:
              self.master.after(100, self.check_queue)

  
    def send_data(self):
      data_to_send = self.send_entry.get()
      print(type(data_to_send))
      if data_to_send:
          self.send_data_queue.put(data_to_send)
          print(f"Enqueued for Sending: {data_to_send}")


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

    def update_stocker_value(self, top_frame):
        self.stocker_frame = StockerApp(top_frame)

    def update_time(self):
        update_time(self.time_label, self.date_label)  # dateTime.pyのupdate_timeを呼び出す

    def start_error_monitoring(self):
        # エラーコードをチェックして、必要に応じてポップアップを表示
        error_code = self.viewmodel.get_error_code()  # ViewModelからエラーコードを取得
        if error_code:
            self.error_popup.show_error(error_code)
        self.master.after(1000, self.start_error_monitoring)  # 1秒ごとにチェック


def start_main_view():
    root = ctk.CTk()
    main_view = MainView(root)
    root.mainloop()
