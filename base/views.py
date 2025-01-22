import customtkinter as ctk
#import tkinter.messagebox as messagebox
#from datetime import datetime
#from PIL import Image
import threading
import queue
import time
#import serial
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

MY_ADDR = 0x05

INPUT_ADDR = 0x01
DISCRIMINATION_ADDR = 0x02
RETURN_ADDR = 0x03
ALIGNMENT_ADDR = 0x04
MASTER_ADDR = 0x06 

STOKER_ADDE = 0x02
POWER_OFF = 0x02


addrList = [
    INPUT_ADDR,DISCRIMINATION_ADDR,RETURN_ADDR,ALIGNMENT_ADDR,MASTER_ADDR,STOKER_ADDE,POWER_OFF
]


structsize = [
0, 2, 2, 3, 2, 4, 4, 3, 2, 12, 3, 3, 3, 4, 5, 2, 3,
2, 5, 4, 2, 2, 2, 2, 2, 3, 2, 3
]

class SerialThread:
  def __init__(self, receive_data_queue,send_data_queue):
    self.receive_data_queue = receive_data_queue
    self.send_data_queue = send_data_queue

    self.serial_test_data = ([0x15,0x0b,0x50],[0x15,0x0b,0x30])
    #try:
    #  self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    #except serial.SerialException as e:
    #  print(f"シリアルポートの初期化に失敗しました: {e}")
    #  self.ser = None

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
          #data_to_send = self.send_data_queue.get_nowait()
          #self.ser.write(data_to_send)
          
     # except queue.Empty:
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

def make_address(myaddress,sendaddress):
  address_send = (myaddress << 4) | sendaddress
  return address_send

def make_send_data(address_send,command,data1=0,data2=0,data3=0):
   send_data = bytearray([address_send,command,data1,data2,data3])
   return send_data


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
        top_frame.pack(fill="x", padx=(0,10), pady=(10, 0))

        # 左側フレーム（時間、日付、投入量）
        left_frame = ctk.CTkFrame(top_frame, fg_color="#2b2b2b")
        left_frame.pack(side="left",padx=0)

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
    
        
      #  send_rebaseInfo()
        
        # 中間ストッカーの残量
        #self.update_stocker_value(top_frame)
        self.stocker_frame = StockerApp(top_frame)

        # 下部フレーム（ボタン）
        self.under_button = UnderButtonFrame(main_frame, self, self.stocker_frame.set_data)

        self.update_time()
        self.sirial_test()
        

        print("done")

    def sirial_test(self):
          photoA_low = 0
          photoA_mid = 1
          photoA_high = 0
          if photoA_low == 1 and photoA_mid == 0 and photoA_high == 0:
              photoA = 0
          elif photoA_low == 0 and photoA_mid == 1 and photoA_high == 0:
              photoA = 0.3
          elif photoA_low == 0 and photoA_mid == 0 and photoA_high == 1:
              photoA = 0.6

          photoB_low = 1
          photoB_mid = 0
          photoB_high = 0
          if photoB_low == 1 and photoB_mid == 0 and photoB_high == 0:
              photoB = 0
          elif photoB_low == 0 and photoB_mid == 1 and photoB_high == 0:
              photoB = 0.3
          elif photoB_low == 0 and photoB_mid == 0 and photoB_high == 1:
              photoB = 0.6
          
          photoC_low = 0
          photoC_mid = 0
          photoC_high = 1
          if photoC_low == 1 and photoC_mid == 0 and photoC_high == 0:
              photoC = 0
          elif photoC_low == 0 and photoC_mid == 1 and photoC_high == 0:
              photoC = 0.3
          elif photoC_low == 0 and photoC_mid == 0 and photoC_high == 1:
              photoC = 0.6

          photo = [photoA, photoB, photoC]
        #   起動時初期化処理
          photo = [0, 0, 0]
          print(photo)
        
          self.stocker_frame.update(photo)
          
    #シリアル通信へのリクエスト
    def check_queue(self):
          try:
            while True:
              data = self.receive_data_queue.get_nowait()
              self.p.set_protocol(data,structsize)
              command = data[1]
            
              if command == INPUTSTOCKERSTATUS:
                self.stocker_capacity = self.p.inputStockerStatus.capacity
                self.update_amount_display(self.amount_label,self.stocker_capacity)

              #elif command == MIDSTOCKERSTATUS:
               #  self.stocker_values = self.p.midStockerStatus.capacity
                # self.update_stocker_value(self, self.stocker_values)
        
              elif command == SENSORINFO:
                print("okkkkkkk")
                data1 = decimalToBinaryList(self.p.s.SensorInfo.data1)
                data2 = decimalToBinaryList(self.p.s.SensorInfo.data2)
                print("data1")                                
                print(data1)
                print("data2")
                print(data2)

                source_address = data[0] >> 4
                print("source_address")
                print(source_address)

                if(source_address == INPUT_ADDR):
                  input_distance = self.p.sensorInfo.data2
                elif(source_address == MASTER_ADDR):#test用にmasterにしてる本来はALIGNMENT_ADDR
                  #先端の供給されたかどうかのセンサ
                  photoA = data1[0]
                  photoB = data1[1]
                  photoC = data1[2]
                  #ストック量
                  photoA_low = data1[3]
                  photoA_mid = data1[4]
                  photoA_high = data1[5]

                  photoB_low = data1[6]
                  photoB_mid = data1[7]
                  photoB_high = data2[0]

                  photoC_low = data2[1]
                  photoC_mid = data2[2]
                  photoC_high = data2[3]
                
                  if photoA_low == 1 and photoA_mid == 0 and photoA_high == 0:
                      photoA = 0
                  elif photoA_low == 0 and photoA_mid == 1 and photoA_high == 0:
                      photoA = 0.3
                  elif photoA_low == 0 and photoA_mid == 0 and photoA_high == 1:
                      photoA = 0.6

                  if photoB_low == 1 and photoB_mid == 0 and photoB_high == 0:
                      photoB = 0
                  elif photoB_low == 0 and photoB_mid == 1 and photoB_high == 0:
                      photoB = 0.3
                  elif photoB_low == 0 and photoB_mid == 0 and photoB_high == 1:
                      photoB = 0.6

                  if photoC_low == 1 and photoC_mid == 0 and photoC_high == 0:
                      photoC = 0
                  elif photoC_low == 0 and photoC_mid == 1 and photoC_high == 0:
                      photoC = 0.3
                  elif photoC_low == 0 and photoC_mid == 0 and photoC_high == 1:
                      photoC = 0.6

                  photo = [photoA, photoB, photoC]
                  self.stocker_frame.update(photo)
                  
          except queue.Empty:
              pass
          finally:
              self.master.after(100, self.check_queue)
    

   # def send_command_SensorInfo(self):
    #    command = INPUTSTOCKERSTATUS

        #for address in addrList:
         #   data_to_send = MY_ADDR + address + command 
          #  print(data_to_send)
            #self.send_data_queue.put(data_to_send)

    def create_amount_display(self, parent_frame):
        # 投入量表示フレームを作成し、単色の背景を追加
        self.amount_frame = ctk.CTkFrame(parent_frame, fg_color="#3A3A3A")  # フレーム全体に単色の背景を設定
        self.amount_frame.pack(side="left", padx=(20,0), pady=(15, 0), expand=True, fill="both")

        self.amount_label = ctk.CTkLabel(self.amount_frame, text="", font=("Arial", 28, "bold"), text_color="#3b8ed0")
        self.amount_label.pack(anchor="center", padx=52, pady=(15, 0))

        self.rate_label = ctk.CTkLabel(self.amount_frame, text="投入口の稼働率", font=("Arial", 12), text_color="#cccccc")
        self.rate_label.pack(anchor="center", padx=45, pady=(0, 5))
        input_amount = 0
        self.amount_label.configure(text=f"投入量 {input_amount}%")
        return self.amount_frame
    
    def update_amount_display(self, amount_label, input_amount):
        amount_label.configure(text=f"投入量 {input_amount}%") 

   # def update_stocker_value(self, stocker_values):
       # self.stocker_frame.set_test(stocker_values)

    def update_time(self):
        update_time(self.time_label, self.date_label)  # dateTime.pyのupdate_timeを呼び出す

    def start_error_monitoring(self):
        # エラーコードをチェックして、必要に応じてポップアップを表示
        error_code = self.viewmodel.get_error_code()  # ViewModelからエラーコードを取得
        if error_code:
            self.error_popup.show_error(error_code)
        self.master.after(1000, self.start_error_monitoring)  # 1秒ごとにチェック

  #シリアル通信送信コマンド
    def send_rebaseInfo(self):
        command = DISCHARGEOPERATION
        for addr in [0x02, 0x03, 0x04]:
            address_send = make_address(MY_ADDR, addr)
            data_to_send = make_send_data(address_send, command)
            self.send_data_queue.put(data_to_send)
        print("排出ボタンが押されました")

    def send_input_start(self):
        command = MODULEOPERATION
        address_send = make_address(MY_ADDR,INPUT_ADDR);
        data_to_send = make_send_data(address_send,command,0x01);
        self.send_data_queue.put(data_to_send)
        print("投入スタートボタンが押されました。")

    def send_input_stop(self):
        command = MODULEOPERATION
        address_send = make_address(MY_ADDR,INPUT_ADDR);
        data_to_send = make_send_data(address_send,command,0x00);
        self.send_data_queue.put(data_to_send)
        print("投入ストップボタンが押されました。")

    def send_discrimination_start(self):
        command = MODULEOPERATION
        address_send = make_address(MY_ADDR,DISCRIMINATION_ADDR);
        data_to_send = make_send_data(address_send,command,0x01);
        self.send_data_queue.put(data_to_send)
        print("判別スタートボタンが押されました。")
    
    def send_discrimination_stop(self):
        command = MODULEOPERATION
        address_send = make_address(MY_ADDR,DISCRIMINATION_ADDR);
        data_to_send = make_send_data(address_send,command,0x00);
        self.send_data_queue.put(data_to_send)
        print("判別ストップボタンが押されました。")

    def send_alignment_start(self):
        command = MODULEOPERATION
        address_send = make_address(MY_ADDR,RETURN_ADDR);
        data_to_send = make_send_data(address_send,command,0x01);
        self.send_data_queue.put(data_to_send)
        print("整列スタートボタンが押されました。")

    def send_alignment_stop(self):
        command = MODULEOPERATION
        address_send = make_address(MY_ADDR,RETURN_ADDR);
        data_to_send = make_send_data(address_send,command,0x00);
        self.send_data_queue.put(data_to_send)
        print("整列ストップボタンが押されました。")

    def send_reabse_start(self):
        command = MODULEOPERATION
        address_send = make_address(MY_ADDR,ALIGNMENT_ADDR);
        data_to_send = make_send_data(address_send,command,0x01);
        self.send_data_queue.put(data_to_send)
        print("返却スタートボタンが押されました。")

    def send_rebase_stop(self):
        command = MODULEOPERATION
        address_send = make_address(MY_ADDR,ALIGNMENT_ADDR);
        data_to_send = make_send_data(address_send,command,0x00);
        self.send_data_queue.put(data_to_send)
        print("返却ストップボタンが押されました。")

    def mastr_stop(self):
        command = MODULEOPERATION
        address_send = make_address(MY_ADDR,MASTER_ADDR);
        data_to_send = make_send_data(address_send,command,0x00);
        self.send_data_queue.put(data_to_send)
        print("全ストップボタンが押されました。")
            
    def send_stocker(self,selected_values):
        print(selected_values)
        command = STOCKERTYPECHANGE
        #自分のaddressと送信先のアドレスを結合すうる
        address_send = make_address(MY_ADDR,STOKER_ADDE);
        #addressとcommandとdataを合体
        data_to_send = make_send_data(address_send,command,selected_values[0],selected_values[1],selected_values[2]);
        print(data_to_send);
        self.send_data_queue.put(data_to_send)
        print("ストッカーの格納先が更新されました")

    def send_shutdown(self):
        command = MODULEOPERATION
        address_send = make_address(MY_ADDR,POWER_OFF);
        data_to_send = make_send_data(address_send,command);
        self.send_data_queue.put(data_to_send)
        print("画像判別モジュールのラズパイをシャットダウンしました！")
    

'''
    def open_maintenance_view(self):
        maintenance_window = ctk.CTkToplevel(self)
        MaintenanceView(maintenance_window, self.on_maintenance_close, self.callback_test, self.callback)

    def on_maintenance_close(self):
        self.deiconify()

    def callback_test(self, data):
        print("data")
'''

def start_main_view():
    root = ctk.CTk()
    main_view = MainView(root)
    root.mainloop()
    

