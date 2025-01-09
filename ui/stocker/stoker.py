import customtkinter as ctk
from ParamManager.ParamManager import ParamManager  
#from ...base.views import MainView
import time
class StockerApp:
    def __init__(self, parent):

        self.stocker_values = [0.9, 0.9, 0.9]
        self.stocker_labels = [2,2,3]#ストッカーの順番
        self.value_labels = [0,0,0]
        self.circles = [0,0,0]
        self.label_buf = [0,0,0]


        self.stocker_frame = ctk.CTkFrame(parent, fg_color="#2b2b2b")
        self.stocker_frame.pack(side="right", expand=True, fill="both", padx=(0, 0), pady=(10, 0))

        ctk.CTkLabel(self.stocker_frame, text="中間ストッカーの残量", font=("Arial", 18, "bold"), text_color="#ffffff").pack(pady=(0, 0))
        self.stocker_grid = ctk.CTkFrame(self.stocker_frame, fg_color="#2b2b2b")
        self.stocker_grid.pack(expand=True, fill="both")

        label_mapping = {
            1: "ボルトM4(5mm)",
            2: "ボルトM4(6mm)",
            3: "ボルトM4(8mm)"
        }
        self.display_labels = [label_mapping[value] for value in self.stocker_labels]
        self.circle_frame = [0,0,0]

        for i, (text, value) in enumerate(zip(self.display_labels, self.stocker_values)):
            self.circle_frame[i] = ctk.CTkFrame(self.stocker_grid, fg_color="#2b2b2b")
            self.circle_frame[i].grid(row=0, column=i, padx=5, pady=0)

            self.canvas = ctk.CTkCanvas(self.circle_frame[i], width=120, height=120, bg="#2b2b2b", highlightthickness=0)
            self.canvas.pack()

            # 背景の円
            self.canvas.create_oval(10, 10, 110, 110, fill="#3A3A3A", outline="")
            
            # 追加: 色を取得するための関数を呼び出す
            text_value, text_color = self.get_text_value(value) 
            color = text_color

            arc = self.canvas.create_arc(10, 10, 110, 110, start=90, extent=-360 * value, fill=color, outline="")
           # self.circles.append([self.canvas, arc])
            self.circles[i] = [self.canvas, arc]
    

            # 中央の円（くり抜き効果）
            self.canvas.create_oval(35, 35, 85, 85, fill="#2b2b2b", outline="")

            # 中央の円の中に表示する値を計算
            percentage_value = f"{value * 100:.0f}%"
            self.value_labels[i] = ctk.CTkLabel(self.circle_frame[i], text=percentage_value, font=("Arial", 20, "bold"), text_color=text_color)
            self.value_labels[i].place(relx=0.5, rely=0.5, anchor="center")
 
            self.label_buf[i] = ctk.CTkLabel(self.stocker_grid, text=text, font=("Arial", 14), text_color="#cccccc", wraplength=120)
            self.label_buf[i].grid(row=1, column=i, padx=5, pady=(5, 0), sticky="nsew")
           # print(self.label_buf[i])

        self.display_labels = [label_mapping[value] for value in self.stocker_labels]

        for i in range(3):
            self.stocker_grid.grid_columnconfigure(i, weight=1)

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

    def update(self, photo):

        for i, (text, value) in enumerate(zip(self.display_labels, self.stocker_values)):
            self.circle_frame[i].destroy()
            self.circle_frame[i] = ctk.CTkFrame(self.stocker_grid, fg_color="#2b2b2b")
            self.circle_frame[i].grid(row=0, column=i, padx=5, pady=0)
            
            self.canvas = ctk.CTkCanvas(self.circle_frame[i], width=120, height=120, bg="#2b2b2b", highlightthickness=0)
            self.canvas.pack()
            self.canvas.create_oval(10, 10, 110, 110, fill="#3A3A3A", outline="")

            # 追加: 色を取得するための関数を呼び出す
            text_value, text_color = self.get_text_value(photo[i])
            color = text_color

            arc = self.canvas.create_arc(10, 10, 110, 110, start=90, extent=-360 * photo[i], fill=color, outline="")
           # self.circles.append([self.canvas, arc])
            self.circles[i] = [self.canvas, arc]
    

            # 中央の円（くり抜き効果）
            self.canvas.create_oval(35, 35, 85, 85, fill="#2b2b2b", outline="")
             # 中央の円の中に表示する値を計算
            percentage_value = f"{photo[i] * 100:.0f}%"
            self.value_labels[i] = ctk.CTkLabel(self.circle_frame[i], text=percentage_value, font=("Arial", 20, "bold"), text_color=text_color)
            self.value_labels[i].place(relx=0.5, rely=0.5, anchor="center")
           # self.value_labels.append(Svalue_label) 

            self.label_buf[i] = ctk.CTkLabel(self.stocker_grid, text=text, font=("Arial", 14), text_color="#cccccc", wraplength=120)
            self.label_buf[i].grid(row=1, column=i, padx=5, pady=(5, 0), sticky="nsew")
