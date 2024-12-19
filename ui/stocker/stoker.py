import customtkinter as ctk
from ParamManager.ParamManager import ParamManager  
import threading
import time

class StockerApp:
    def __init__(self, parent):
        self.param_manager = ParamManager()
        self.stocker_values = self.param_manager.get_stocker_values()
        self.stocker_labels = [2,2,3]#self.param_manager.get_stocker_pos()
        self.value_labels = []
        self.circles = []
        self.label_buf = [0,0,0]
        self.create_stocker_frame(parent)

    def create_stocker_frame(self, parent):
        stocker_frame = ctk.CTkFrame(parent, fg_color="#2b2b2b")
        stocker_frame.pack(side="right", expand=True, fill="both", padx=(0, 0), pady=(10, 0))

        ctk.CTkLabel(stocker_frame, text="中間ストッカーの残量", font=("Arial", 18, "bold"), text_color="#ffffff").pack(pady=(0, 0))

        stocker_grid = ctk.CTkFrame(stocker_frame, fg_color="#2b2b2b")
        stocker_grid.pack(expand=True, fill="both")

        label_mapping = {
            1: "ボルトM4(5mm)",
            2: "ボルトM4(6mm)",
            3: "ボルトM4(8mm)"
        }

        # 追加: stocker_labelsに基づいて表示するラベルを設定
        self.display_labels = [label_mapping[value] for value in self.stocker_labels]

        for i, (text, value) in enumerate(zip(self.display_labels, self.stocker_values)):
            circle_frame = ctk.CTkFrame(stocker_grid, fg_color="#2b2b2b")
            circle_frame.grid(row=0, column=i, padx=5, pady=0)

            canvas = ctk.CTkCanvas(circle_frame, width=120, height=120, bg="#2b2b2b", highlightthickness=0)
            canvas.pack()

            # 背景の円
            canvas.create_oval(10, 10, 110, 110, fill="#3A3A3A", outline="")
            
            # 追加: 色を取得するための関数を呼び出す
            text_value, text_color = self.get_text_value(value)  # 新しい関数を作成
            color = text_color  # ここでcolorを定義

            arc = canvas.create_arc(10, 10, 110, 110, start=90, extent=-360 * value, fill=color, outline="")
            self.circles.append((canvas, arc))  # 追加: 円の情報を保持

            # 中央の円（くり抜き効果）
            canvas.create_oval(35, 35, 85, 85, fill="#2b2b2b", outline="")

            # 中央の円の中に表示する値を計算
            percentage_value = f"{value * 100:.0f}%"
            Svalue_label = ctk.CTkLabel(circle_frame, text=percentage_value, font=("Arial", 20, "bold"), text_color=text_color)
            Svalue_label.place(relx=0.5, rely=0.5, anchor="center")
            self.value_labels.append(Svalue_label)  # 追加: ラベルの情報を保持

            self.label_buf[i] = ctk.CTkLabel(stocker_grid, text=text, font=("Arial", 14), text_color="#cccccc", wraplength=120)
            self.label_buf[i].grid(row=1, column=i, padx=5, pady=(5, 0), sticky="nsew")
            print(self.label_buf[i])

        for i in range(3):
            stocker_grid.grid_columnconfigure(i, weight=1)

        #threading.Thread(target=self.update_stocker_values, args=(self.param_manager,), daemon=True).start()

    def set_data(self, pos_data):
        self.pos_data:int = pos_data
        label_mapping = {
            0: "ボルトM4(5mm)",
            1: "ボルトM4(6mm)",
            2: "ボルトM4(8mm)"
        }

        for i in range(3):
            self.label_buf[i].configure(text=f"{label_mapping[pos_data[i]]}")

    def get_text_value(self, value):
        if value == 0:
            return "なし", "#ffffff"
        elif 0.1 <= value <= 0.3:
            return "小", "#00ff00"
        elif 0.3 < value <= 0.7:
            return "中", "#3b8ed0"
        else:
            return "強", "#ff0000"

    def update_stocker_values(self, param_manager):
        while True:
            stocker_values = param_manager.get_stocker_values() 
            for i, value in enumerate(stocker_values):
              
                text_value, text_color = self.get_text_value(value)
                self.value_labels[i].configure(text=f"{value * 100:.0f}%", text_color=text_color)

                canvas, arc = self.circles[i]
                canvas.itemconfig(arc, extent=-360 * value)

            time.sleep(5)

