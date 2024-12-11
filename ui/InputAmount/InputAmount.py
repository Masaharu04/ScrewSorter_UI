import customtkinter as ctk  # customtkinterをインポート
from ParamManager.ParamManager import ParamManager  # ParamManagerをインポート
import threading  # 追加
import time  # 追加

class InputAmountFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#3A3A3A")
        self.pack(anchor="center", padx=10, pady=0)

        self.param_manager = ParamManager()  # ParamManagerのインスタンスを作成
        self.amount_label = ctk.CTkLabel(self, text="", font=("Arial", 28, "bold"), text_color="#3b8ed0")
        self.amount_label.pack(anchor="center", padx=35, pady=(15, 0))

        self.rate_label = ctk.CTkLabel(self, text="投入口の稼働率", font=("Arial", 12), text_color="#cccccc")
        self.rate_label.pack(anchor="center", padx=5, pady=(0, 5))

        # 初期表示の更新
        self.update_input_amount()  # 初期値を表示
       # threading.Thread(target=self.run_update, daemon=True).start()  # スレッドを開始

    def update_input_amount(self):
        #input_amount = self.param_manager.get_input_amount()  # 投入量を取得
        input_amount = 10
        self.amount_label.configure(text=f"投入量 {input_amount}%")  # ラベルを更新

   # def run_update(self):
    #    while True:
     #       self.update_input_amount()  # 定期的に更新
      #      time.sleep(5)  # 5秒ごとに更新
