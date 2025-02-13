import customtkinter as ctk
from PIL import Image
import threading
import time
from ui.export.export import export_button_action
from ui.Shutdown.Shutdown import ShutdownPopup  # ShutdownPopupクラスをインポート
from base.settingviews import SettingViews  # MaintenanceViewをインポート
from base.menteviews import MaintenanceView
from base.mentemainview import MaintenanceMainView
from ParamManager.ParamManager import ParamManager 
from base.timesettingview import TimeSettingView
from send_data import SendModuleOperation

class UnderButtonFrame:
    def __init__(self, master, main_view, stocker_data_buf,send_rebaseInfo,request_output_csv):
        self.master = master
        self.main_view = main_view
        self.button_enabled = {}  # 各ボタンの有効/無効状態を管理
        self.shutdown_popup = ShutdownPopup(master)  # ShutdownPopupのインスタンスを作成
        self.setup_buttons()
        self.stocker_data_buf = stocker_data_buf
        
        self.send_rebaseInfo = send_rebaseInfo
        self.request_output_csv = request_output_csv
        self.send_module_operation = SendModuleOperation()

        self.motervalue = [4,6,4]

    def setup_buttons(self):
        # ボタンフレーム
        self.button_frame = ctk.CTkFrame(self.master, fg_color="#2b2b2b")
        self.button_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ボタン用の画像を読み込む
        self.button_image = ctk.CTkImage(Image.open("img/settings.png"), size=(60, 60))
        self.poweroff_image = ctk.CTkImage(Image.open("img/poweroff.png"), size=(40, 40))
        self.clock_image = ctk.CTkImage(Image.open("img/clock.png"), size=(45, 45))
        self.discharge_image = ctk.CTkImage(Image.open("img/exsit.png"), size=(40, 40))
        self.export_image = ctk.CTkImage(Image.open("img/export.png"), size=(60, 60))
        self.maintenance_image = ctk.CTkImage(Image.open("img/maintenance.png"), size=(50, 50))
        

        # ボタン設定
        self.buttons = [
            ("設定", "#3b8ed0", lambda: self.handle_button_click("設定", self.open_setting_view, False)),
            ("排出", "#3b8ed0", lambda: self.handle_button_click("排出", self.discharge_operation, True)),
            ("時刻設定", "#3b8ed0", lambda: self.handle_button_click("時刻設定", self.open_timesetting_view, True)),
            ("エクスポート", "#1f6aa5", lambda: self.handle_button_click("エクスポート", self.export_button_action, True)),
            ("メンテナンス", "#1f6aa5", lambda: self.handle_button_click("メンテナンス", self.open_maintenance_view, False)),
             ("シャットダウン", "#FF5216", lambda: self.handle_button_click("シャットダウン", self.open_shutdown_confirmation, False))
           
        ]

        # 各ボタンの初期状態を有効に設定
        for button_name, _, _ in self.buttons:
            self.button_enabled[button_name] = True

        self.create_buttons()

    def export_button_action(self):
        self.request_output_csv()
        print("エクスポート")

    def callback_test(self,data):
        print("data...........................")
        
    def handle_button_click(self, button_name, command, use_timer):
        if self.button_enabled[button_name]:
            if use_timer:
                self.button_enabled[button_name] = False
            command()
            if use_timer:
                threading.Thread(target=lambda: self.enable_button_after_delay(button_name)).start()

    def enable_button_after_delay(self, button_name):
        time.sleep(3)  # 3秒間待機
        self.button_enabled[button_name] = True

    def create_buttons(self):
        for i, (text, color, command) in enumerate(self.buttons):
            button_frame_inner = ctk.CTkFrame(self.button_frame, fg_color=color, corner_radius=10)
            button_frame_inner.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")
            
            # 中央配置用のフレーム
            center_frame = ctk.CTkFrame(button_frame_inner, fg_color=color)
            center_frame.place(relx=0.5, rely=0.5, anchor="center")
            
            # 画像の選択
            if text == "設定":
                button_image = self.button_image
            elif text == "一連動作":
                button_image = self.cycle_image
            elif text == "排出":
                button_image = self.discharge_image
            elif text == "エクスポート":
                button_image = self.export_image
            elif text == "メンテナンス":
                button_image = self.maintenance_image
            elif text == "シャットダウン": 
                button_image = self.poweroff_image
            else:
                 button_image = self.clock_image
            
            # 画像ボタン
            image_button = ctk.CTkLabel(
                center_frame, 
                image=button_image,
                text="",
                fg_color=color,
               # hover_color=None,  # ホバー時の色を無効にする
                width=40,
                height=40,
                corner_radius=10
            )
            image_button.pack()
            
            # テキストラベル
            text_label = ctk.CTkLabel(
                center_frame,
                text=text,
                font=("Futura", 14, "bold"),
                text_color="#ffffff"
            )
            text_label.pack()
            
            # クリックイベントをフレーム全体に設定
            button_frame_inner.bind("<Button-1>", lambda e, cmd=command: cmd())
            image_button.bind("<Button-1>", lambda e, cmd=command: cmd())
            text_label.bind("<Button-1>", lambda e, cmd=command: cmd())

        # グリッドの設定
        for i in range(3):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            self.button_frame.grid_rowconfigure(i, weight=1)

    def open_shutdown_confirmation(self):
        # シャットダウン確認ポップアップを表示
        self.shutdown_popup.shutdown_button_action()  # インスタンスメソッドを呼び出す

    def print_operation(self):
        print("一連動作ボタンが押されました")  # 一連動作ボタンが押されたときの処理

    def discharge_operation(self):
      # 排出ボタンが押されたときの処理
       self.send_rebaseInfo()

    def open_maintenance_view(self):
        # メンテナンス画面を開く
        maintenance_window = ctk.CTkToplevel(self.master)
        MaintenanceMainView(maintenance_window, self.on_maintenance_close,self.motervalue)  # send_input_startをコールバックとして渡す
        print("llllllllllllllllllll")       
        print(self.motervalue)
    def on_maintenance_close(self):
        # self.master.deiconify()
        self.master.pack() 

    def open_setting_view(self):
        # 設定画面を開く
        setting_window = ctk.CTkToplevel(self.master)  # CTkウィンドウを作成
        SettingViews(setting_window, self.on_setting_close,self.callback_test, self.stocker_data_buf)  # MaintenanceViewを開く

    def open_timesetting_view(self):
        timeSetting_window = ctk.CTkToplevel(self.master)
        TimeSettingView(timeSetting_window)

    def on_setting_close(self):       
        # self.master.deiconify()
        self.master.pack()
