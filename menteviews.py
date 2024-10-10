# menteviews.py
import customtkinter as ctk

class MaintenanceView:
    def __init__(self, master, on_close):
        self.master = master
        self.on_close = on_close  # メインウィンドウを再表示するためのコールバック
        self.setup_ui()

    def setup_ui(self):
        self.master.title("メンテナンス画面")
        # フルスクリーンで表示
        self.master.attributes('-fullscreen', True)
        self.master.overrideredirect(True)  # ウィンドウのバーを非表示

        label = ctk.CTkLabel(self.master, text="メンテナンス画面へようこそ！", font=("Arial", 18))
        label.pack(pady=50)

        close_button = ctk.CTkButton(self.master, text="戻る", command=self.close_maintenance_view)  # 戻るボタンにコールバックを設定
        close_button.pack(pady=20)

    def close_maintenance_view(self):
        self.master.destroy()  # メンテナンス画面を閉じる
        self.on_close()  # メインウィンドウを再表示するためのコールバックを呼び出す
