import customtkinter as ctk
from ParamManager.ParamManager import ParamManager  # ParamManagerをインポート

def create_stocker_frame(parent):
    stocker_frame = ctk.CTkFrame(parent, fg_color="#2b2b2b")
    stocker_frame.pack(side="right", expand=True, fill="both", padx=(0, 0), pady=(10, 0))

    ctk.CTkLabel(stocker_frame, text="中間ストッカーの残量", font=("Arial", 18, "bold"), text_color="#ffffff").pack(pady=(0, 0))

    stocker_grid = ctk.CTkFrame(stocker_frame, fg_color="#2b2b2b")
    stocker_grid.pack(expand=True, fill="both")

    param_manager = ParamManager()  # ParamManagerのインスタンスを作成
    stocker_values = param_manager.get_stocker_values()  # ストッカーの値を取得
    stocker_labels = ["ボルトM4(5mm)", "ボルトM4(6mm)", "ボルトM4(8mm)"]
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

    for i in range(3):
        stocker_grid.grid_columnconfigure(i, weight=1)