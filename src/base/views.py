import customtkinter as ctk
import tkinter.messagebox as messagebox
from datetime import datetime
from PIL import Image
from src.viewmodels import MainViewModel
from src.base.menteviews import MaintenanceView  
from src.ui.UnderButton.UnderButton import UnderButtonFrame
from src.ui.EarPop.EarPopup import ErrorPopup

class MainView:
    def __init__(self, master):
        self.master = master
        self.viewmodel = MainViewModel()
        self.error_popup = ErrorPopup(master)
        self.error_popup.set_viewmodel(self.viewmodel)
        self.setup_ui()
        self.start_error_monitoring()

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

        # 時間表示
        self.time_label = ctk.CTkLabel(left_frame, text="10:55", font=("Arial", 60, "bold"), text_color="#ffffff")
        self.time_label.pack(anchor="center", pady=(0, 0))

        # 日付表示
        self.date_label = ctk.CTkLabel(left_frame, text="8月27日火曜日", font=("Arial", 18), text_color="#cccccc")
        self.date_label.pack(anchor="center", pady=(0, 5))
        # 投入量表示
        input_amount_frame = ctk.CTkFrame(left_frame, fg_color="#3A3A3A")
        input_amount_frame.pack(anchor="center", padx=10, pady=0)

        ctk.CTkLabel(input_amount_frame, text="投入量 24%", font=("Arial", 28, "bold"), text_color="#3b8ed0").pack(anchor="center", padx=35, pady=(15,0))
        ctk.CTkLabel(input_amount_frame, text="投入口の稼働率", font=("Arial", 12), text_color="#cccccc").pack(anchor="center", padx=5, pady=(0,5))

        # 中間ストッカーの残量表示フレーム
        stocker_frame = ctk.CTkFrame(top_frame, fg_color="#2b2b2b")
        stocker_frame.pack(side="right", expand=True, fill="both", padx=(0, 0),pady=(10,0))

        ctk.CTkLabel(stocker_frame, text="中間ストッカーの残量", font=("Arial", 18, "bold"), text_color="#ffffff").pack(pady=(0, 0))

        stocker_grid = ctk.CTkFrame(stocker_frame, fg_color="#2b2b2b")
        stocker_grid.pack(expand=True, fill="both")
        stocker_values = [0, 0.3, 0.6, 0.9]  # 各ストッカーの値を設定
        stocker_labels = ["ボルトM4(5mm)", "ボルトM4(6mm)", "ボルトM4(8mm)", "その他"]
        color = "#3b8ed0"  # 単色の設定

        for i, (text, value) in enumerate(zip(stocker_labels, stocker_values)):
            circle_frame = ctk.CTkFrame(stocker_grid, fg_color="#2b2b2b")
            circle_frame.grid(row=0, column=i, padx=5, pady=0)

            canvas = ctk.CTkCanvas(circle_frame, width=120, height=120, bg="#2b2b2b", highlightthickness=0)
            canvas.pack()

            # 背景の円
            canvas.create_oval(10, 10, 110, 110, fill="#3A3A3A", outline="")
            
            # 進捗を示す円弧
            canvas.create_arc(10, 10, 110, 110, start=90, extent=-360*value, fill=color, outline="")
            
            # 中央の円（くり抜き効果）
            canvas.create_oval(35, 35, 85, 85, fill="#2b2b2b", outline="")

            if value == 0:
                text_value = "なし"
                text_color = "#ffffff"
            elif 0.1 <= value <= 0.3:
                text_value = "小"
                text_color = "#00ff00"
            elif 0.3 < value <= 0.7:
                text_value = "中"
                text_color = "#3b8ed0"
            else:
                text_value = "強"
                text_color = "#ff0000"

            Svalue_label = ctk.CTkLabel(circle_frame, text=text_value, font=("Arial", 20, "bold"), text_color=text_color)
            Svalue_label.place(relx=0.5, rely=0.5, anchor="center")

            label = ctk.CTkLabel(stocker_grid, text=text, font=("Arial", 14), text_color="#cccccc", wraplength=120)
            label.grid(row=1, column=i, padx=5, pady=(5, 0), sticky="nsew")

        for i in range(4):
            stocker_grid.grid_columnconfigure(i, weight=1)

        # 下部フレーム（ボタン）
        self.under_button = UnderButtonFrame(main_frame, self)

        self.update_time()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%m月%d日(%a)").replace("Mon", "月").replace("Tue", "火").replace("Wed", "水").replace("Thu", "").replace("Fri", "金").replace("Sat", "土").replace("Sun", "日")
        self.time_label.configure(text=f"{current_time}")
        self.date_label.configure(text=f"{current_date}")
        self.master.after(1000, self.update_time)

    def display_message(self, text):
        print(text)  # メッセージをコンソールに出力

    def show_warning(self):
        # テスト用にエラーコードをセット
        self.viewmodel.set_error_code("E001")

    def on_settings_close(self):
        self.master.deiconify()

    def open_maintenance_view(self):
        self.master.withdraw()
        maintenance_window = ctk.CTkToplevel(self.master)
        MaintenanceView(maintenance_window, self.on_maintenance_close)

    def on_maintenance_close(self):
        self.master.deiconify()

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
