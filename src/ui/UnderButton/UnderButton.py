import customtkinter as ctk
from PIL import Image
import threading
import time
from src.ui.export.export import export_button_action
from src.ui.Shutdown.Shutdown import ShutdownPopup  # ShutdownPopupクラスをインポート
from src.base.settingviews import MaintenanceView  # MaintenanceViewをインポート

class UnderButtonFrame:
    def __init__(self, master, main_view):
        self.master = master
        self.main_view = main_view
        self.button_enabled = {}  # 各ボタンの有効/無効状態を管理
        self.shutdown_popup = ShutdownPopup(master)  # ShutdownPopupのインスタンスを作成
        self.setup_buttons()

    def setup_buttons(self):
        # ボタンフレーム
        self.button_frame = ctk.CTkFrame(self.master, fg_color="#2b2b2b")
        self.button_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ボタン用の画像を読み込む
        self.button_image = ctk.CTkImage(Image.open("img/settings.png"), size=(60, 60))
        self.poweroff_image = ctk.CTkImage(Image.open("img/poweroff.png"), size=(40, 40))
        self.cycle_image = ctk.CTkImage(Image.open("img/cycle.png"), size=(50, 50))
        self.discharge_image = ctk.CTkImage(Image.open("img/exsit.png"), size=(40, 40))
        self.export_image = ctk.CTkImage(Image.open("img/export.png"), size=(60, 60))
        self.maintenance_image = ctk.CTkImage(Image.open("img/maintenance.png"), size=(50, 50))

        # ボタン設定
        self.buttons = [
            ("設定", "#3b8ed0", lambda: self.handle_button_click("設定", self.open_setting_view, False)),
            ("一連動作", "#3b8ed0", lambda: self.handle_button_click("一連動作", lambda: self.main_view.display_message("一連動作ボタンが押されました"), True)),
            ("排出", "#3b8ed0", lambda: self.handle_button_click("排出", lambda: self.main_view.display_message("排出ボタンが押されました"), True)),
            ("エスポート", "#1f6aa5", lambda: self.handle_button_click("エスポート", export_button_action, True)),
            ("メンテナンス", "#1f6aa5", lambda: self.handle_button_click("メンテナンス", self.main_view.open_maintenance_view, False)),
            ("シャットダウン", "#FF5216", lambda: self.handle_button_click("シャットダウン", self.open_shutdown_confirmation, False))
        ]

        # 各ボタンの初期状態を有効に設定
        for button_name, _, _ in self.buttons:
            self.button_enabled[button_name] = True

        self.create_buttons()

    def open_setting_view(self):
        # 設定画面を開く
        setting_window = ctk.CTkToplevel(self.master)
        MaintenanceView(setting_window, self.on_setting_close)  # MaintenanceViewを開く
        self.master.withdraw()  # 元のウィンドウを隠す

    def on_setting_close(self):
        self.master.deiconify()  # 元のウィンドウを再表示

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
            elif text == "エスポート":
                button_image = self.export_image
            elif text == "メンテナンス":
                button_image = self.maintenance_image
            else:  # シャットダウン
                button_image = self.poweroff_image
            
            # 画像ボタン
            image_button = ctk.CTkButton(
                center_frame, 
                image=button_image,
                text="",
                fg_color=color,
                hover_color=None,  # ホバー時の色を無効にする
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