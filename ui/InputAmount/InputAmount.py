import customtkinter as ctk  # customtkinterをインポート
from ParamManager.ParamManager import ParamManager  # ParamManagerをインポート

class InputAmountFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#3A3A3A")
        self.pack(anchor="center", padx=10, pady=0)

        self.param_manager = ParamManager()  # ParamManagerのインスタンスを作成
        input_amount = self.param_manager.get_input_amount()  # 投入量を取得

        # 投入量表示
        self.amount_label = ctk.CTkLabel(self, text=f"投入量 {input_amount}%", font=("Arial", 28, "bold"), text_color="#3b8ed0")
        self.amount_label.pack(anchor="center", padx=35, pady=(15, 0))

        self.rate_label = ctk.CTkLabel(self, text="投入口の稼働率", font=("Arial", 12), text_color="#cccccc")
        self.rate_label.pack(anchor="center", padx=5, pady=(0, 5))
