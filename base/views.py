import customtkinter as ctk
#import tkinter.messagebox as messagebox
#from datetime import datetime
#from PIL import Image
import threading
import queue
import time
import datetime
#import serial
from viewmodels import MainViewModel
from base.menteviews import MaintenanceView  
from ui.UnderButton.UnderButton import UnderButtonFrame
from ui.EarPop.EarPopup import ErrorPopup
from ..ui.stocker.stoker import StockerApp
from ui.dateTime.dateTime import update_time  # dateTime.pyのupdate_timeをインポート
from ui.InputAmount.InputAmount import InputAmountFrame  # InputAmount.pyのInputAmountFrameをインポート
from struct_command import *
from ..struct_command import *
from CsvClass import CsvControl
from base import config

AAAAAAAAAAA = 'csv_data/'
DIR_PATH = AAAAAAAAAAA + 'testdata/'
USB_DIR_PATH = AAAAAAAAAAA + 'outputdata/'
DISCRIMINATION_RESULTS_FILE_PATH = DIR_PATH + 'discrimination_results.csv'
DATA2_FILE_PATH = DIR_PATH + 'data2.csv'
DATA3_FILE_PATH = DIR_PATH + 'data3.csv'
DISCRIMINATION_RESULTS_HEADER = ['Time', 'Thickness', 'length']
DATA2_HEADER = ['Time', 'M5*8', 'M5*10', 'M5*12', 'M5*16', 'M6*8', 'M6*10', 'M6*12', 'M6*16', 'return', 'etc']
DATA3_HEADER = DATA2_HEADER


SERIAL_PORT = '/dev/ttyS0'
BAUD_RATE = 115200

MY_ADDR = 0x05

INPUT_ADDR = 0x01
DISCRIMINATION_ADDR = 0x02
RETURN_ADDR = 0x03
ALIGNMENT_ADDR = 0x04
MASTER_ADDR = 0x06 
OUTPUT_ADDR = 0x08
IMAGE_ADDR = 0x09


STOKER_ADDE = 0x02
POWER_OFF = 0x02


addrList = [
    INPUT_ADDR,DISCRIMINATION_ADDR,RETURN_ADDR,ALIGNMENT_ADDR,MASTER_ADDR,OUTPUT_ADDR,IMAGE_ADDR
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
          data_to_send = self.send_data_queue.get_nowait()
          print("//////////send//////////")
          print(data_to_send)
          #self.ser.write(data_to_send)
          
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
        now = datetime.datetime.now()
        format_now = now.strftime("%Y/%m/%d/%H/%M")
        self.csv_test = CsvControl(format_now, DIR_PATH, USB_DIR_PATH, DISCRIMINATION_RESULTS_FILE_PATH, DATA2_FILE_PATH, DATA3_FILE_PATH
                   , DISCRIMINATION_RESULTS_HEADER, DATA2_HEADER, DATA3_HEADER)

        self.MODULE_ADDRESSES = [INPUT_ADDR, DISCRIMINATION_ADDR, RETURN_ADDR, ALIGNMENT_ADDR, MASTER_ADDR, OUTPUT_ADDR]
        #接続確認応答フラグ
        self.received_module_flag = {addr: False for addr in self.MODULE_ADDRESSES}
        self.received_flags = False
        #self.send_check_commands()
        # カーソルを非表示にする
        self.master.config(cursor="")
        self.stocker_data_buf = [0,0,0]
        
        self.errorpop_flag = False
        self.error_bandle = ["","E010","E011","E012","E013","","","","","","","",""]
        
        self.setup_ui()
        self.start_error_monitoring()

        print("初期動作完了")

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
        ####################################################################  
        #キューの初期化
        # self.receive_data_queue = queue.Queue()
        # self.send_data_queue = queue.Queue()
        self.receive_data_queue = config.receive_data_queue
        self.send_data_queue = config.send_data_queue
        #################################################################### 
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
        self.stocker_frame = StockerApp(top_frame)
        
        self.stocker_data_buf.append(ctk.IntVar())
        self.stocker_data_buf[3].set(0)
        self.stocker_data_buf[3].trace_add("write", self.stocker_callback)

        # 下部フレーム（ボタン）
        self.under_button = UnderButtonFrame(main_frame, self, self.stocker_data_buf,self.send_rebaseInfo,self.csv_test.request_output_csv)

        self.update_time()
        self.sirial_test()
        
        print("初期動作完了")
    
    def stocker_callback(self, *arg):
        print("aaaaaaaaaa")
        buf = [0,0,0]
        for i in range(0,3):
            buf[i] = self.stocker_data_buf[i]
        self.stocker_frame.set_data(buf)
        
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
          print("起動時",photo)
        
          self.stocker_frame.update(photo)
          
    #シリアル通信へのリクエスト
    def check_queue(self):
          try:
            while True:
              print("check_queue")
              now = datetime.datetime.now()
              format_now = now.strftime("%Y/%m/%d/%H/%M")
              self.csv_test.csv_controller(format_now)
              
              data = self.receive_data_queue.get_nowait()
              self.p.set_protocol(data,structsize)
              command = data[1]

              if command == DISCRIMINATIONRESULT:
                 self.write_discrimination_result(data[2])

              if self.errorpop_flag:
                for addr in self.MODULE_ADDRESSES:
                    if False == self.received_module_flag[addr]:
                        self.error_popup.show_error(self.error_bandle[addr])
                self.errorpop_flag = False
                 
              #接続確認応答      
              if not self.received_flags:    
                    self.send_check_commands()#各スレーブにリクエスト送信
                    self.received_flags = True
                    self.wait_for_responses()
            
            #   if command == INPUTSTOCKERSTATUS:
            #      self.stocker_capacity = self.p.inputStockerStatus.capacity
            #      self.update_amount_display(self.amount_label,self.stocker_capacity)

            #   el
              if command == SENSORINFO:
                data1 = decimalToBinaryList(self.p.s.SensorInfo.data1)
                data2 = decimalToBinaryList(self.p.s.SensorInfo.data2)
                source_address = data[0] >> 4
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
                  photoB_high = data2[4]

                  photoC_low = data2[5]
                  photoC_mid = data2[6]
                  photoC_high = data2[7]
                
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
              
    def send_check_commands(self):
        """ 各モジュールに接続確認コマンドを送信 """
        for addr in self.MODULE_ADDRESSES:
            print(f"モジュール {hex(addr)} の接続確認を開始")  
            command = CONNECTCHECK
            address_send = make_address(MY_ADDR, addr)
            data_to_send = make_send_data(address_send, command)
            self.send_data_queue.put(data_to_send)
            print(f"送信: {data_to_send}")

    def write_discrimination_result(self, result_data):
        if result_data in [0x01, 0x02, 0x03]:
            now = datetime.datetime.now()
            format_now = now.strftime("%Y/%m/%d/%H/%M")
            stocker_data = self.stocker_data_buf[result_data-1]
            STOCKERLABELS = [[5, 8], [5, 10], [5, 12],[5, 16], 
                [6, 8], [6, 10], [6, 12], [6, 16]]
            csv_data = [format_now] + STOCKERLABELS[stocker_data]
            print(csv_data)
            self.csv_test.add_a_line_of_csv_data(DISCRIMINATION_RESULTS_FILE_PATH, csv_data)
        elif result_data == 0x04:
            now = datetime.datetime.now()
            format_now = now.strftime("%Y/%m/%d/%H/%M")
            csv_data = [format_now, 0, 0]
            print(csv_data)
            self.csv_test.add_a_line_of_csv_data(DISCRIMINATION_RESULTS_FILE_PATH, csv_data)
        elif result_data == 0x05:
            now = datetime.datetime.now()
            format_now = now.strftime("%Y/%m/%d/%H/%M")
            csv_data = [format_now, -1, -1]
            print(csv_data)
            self.csv_test.add_a_line_of_csv_data(DISCRIMINATION_RESULTS_FILE_PATH, csv_data) 

        
    def wait_for_responses(self, timeout=5):
        """ 応答を5秒間待機し、接続確認を行う """
        start_time = time.time()
        received_addresses = set()
        
        while time.time() - start_time < timeout:
            try:
                # 受信データを取得（最大0.5秒待つ）
                data = self.receive_data_queue.get(timeout=0.5)
                command = data[1]
                source_address = data[0] >> 4

                if command == CONNECTCHECKRESPONSE and source_address in self.MODULE_ADDRESSES:
                    self.received_module_flag[source_address] = True  # 応答を受け取ったモジュールをマーク
                    received_addresses.add(source_address)
                    print(f"モジュール {hex(source_address)} 接続完了")

                # すべてのモジュールから応答を受け取ったら終了
                if len(received_addresses) == len(self.MODULE_ADDRESSES):
                    print("全モジュール接続確認完了")
                    # self.response_received = True  # 応答を受信したことを記録
                    return True

            except queue.Empty:
                continue  # タイムアウトまで待機

        # 応答がなかったモジュールのエラー処理
        missing_addresses = [addr for addr, received in self.received_module_flag.items() if not received]
        if missing_addresses:
            print(f"エラー: 接続確認ができなかったモジュール {', '.join(hex(addr) for addr in missing_addresses)}")
            self.errorpop_flag = True
            

        # self.response_received = True  # 応答を受信したことを記録
        return False
   
    def show_error_popup(self, error_code):
        """ エラーポップを表示する（仮のprint出力）"""
        print(f"[ERROR] {error_code}: 接続確認エラーが発生しました")

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

    def update_time(self):
        update_time(self.time_label, self.date_label)  # dateTime.pyのupdate_timeを呼び出す

    def start_error_monitoring(self):

        # エラーコードをチェックして、必要に応じてポップアップを表示
        error_code = self.viewmodel.get_error_code()  # ViewModelからエラーコードを取得
        if error_code:
            self.error_popup.show_error(error_code)
        self.master.after(1000, self.start_error_monitoring)  # 1秒ごとにチェック

        command = CONNECTCHECK
        address_send = make_address(MY_ADDR,INPUT_ADDR);
        data_to_send = make_send_data(address_send,command);
        # self.send_data_queue.put(data_to_send)#エラーコマンドリクエスト

  #シリアル通信送信コマンド
    def send_rebaseInfo(self):
        command = DISCHARGEOPERATION
        for addr in [0x02, 0x03, 0x04]:
            address_send = make_address(MY_ADDR, addr)
            data_to_send = make_send_data(address_send, command)
            self.send_data_queue.put(data_to_send)
        print("排出ボタンが押されました")
            
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

def start_main_view():
    root = ctk.CTk()
    main_view = MainView(root)
    root.mainloop()
    
