import customtkinter as ctk
import tkinter.messagebox as messagebox
from viewmodels import MainViewModel  # ViewModel をインポート
from menteviews import MaintenanceView  # MenteViewをインポート

class MainView:
    def __init__(self, master):
        self.master = master
        self.viewmodel = MainViewModel()  # ViewModelのインスタンス化
        self.setup_ui()

    def setup_ui(self):
        # ウィンドウサイズを800x400に設定
        self.master.geometry('800x400')
        self.master.title("メイン画面")
        self.master.overrideredirect(True)  # ウィンドウのバーを非表示

        # ダークテーマとカスタムカラーの設定
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # 上部フレームの設定（中央に配置）
        top_frame = ctk.CTkFrame(self.master, corner_radius=15)
        top_frame.pack(padx=10, pady=10, expand=False, fill="both")  # 少しコンパクトに調整

        # フレーム全体を中央に寄せるための設定
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=1)

        # ボルトサイズ表示のラベル（フォントサイズを少し調整）
        label_a = ctk.CTkLabel(top_frame, text="A\nボルト M4 (5mm)", font=("Arial", 20))  # フォントサイズを小さめに
        label_a.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        label_b = ctk.CTkLabel(top_frame, text="B\nボルト M4 (6mm)", font=("Arial", 20))  # フォントサイズを小さめに
        label_b.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        label_c = ctk.CTkLabel(top_frame, text="C\nボルト M4 (8mm)", font=("Arial", 20))  # フォントサイズを小さめに
        label_c.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # ボタンフレームの設定（中央に配置）
        button_frame = ctk.CTkFrame(self.master, corner_radius=15)
        button_frame.pack(padx=10, pady=10, expand=True, fill="both")  # コンパクトなマージン設定

        # 各種ボタンの作成（小さめのサイズで設定）
        buttons = [
            ("設定", "#3b8ed0", lambda: (self.show_warning(), self.display_message("設定ボタンが押されました"))),
            ("一度操作", "#3b8ed0", lambda: self.display_message("一度操作ボタンが押されました")),
            ("排出", "#3b8ed0", lambda: self.display_message("排出ボタンが押されました")),
            ("エクスポート", "#1f6aa5", lambda: self.display_message("エクスポートボタンが押されました")),
            ("メンテナンス", "#1f6aa5", self.open_maintenance_view),
            ("シャットダウン", "#ff4d4d", lambda: self.display_message("シャットダウンボタンが押されました"))
        ]

        # ボタンの配置（行列レイアウトとサイズ調整）
        for i, (text, color, command) in enumerate(buttons):
            button = ctk.CTkButton(button_frame, text=text, width=200, height=100, corner_radius=15, fg_color=color, command=command)
            button.grid(row=i // 3, column=i % 3, padx=10, pady=10)  # パディング調整

        # 各ラベルが均等に配置されるように設定
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        # メッセージ表示用のラベル
        self.output_label = ctk.CTkLabel(self.master, text="", font=("Arial", 18))  # フォントサイズを少し小さめに
        self.output_label.pack(pady=10)

    def display_message(self, text):
        self.output_label.configure(text=text)

    # 警告ポップアップを表示する関数
    def show_warning(self):
        messagebox.showwarning("警告", "設定を変更しようとしています。よろしいですか？")

    def open_maintenance_view(self):
        """メンテナンス画面を開く"""
        self.master.withdraw()  # メイン画面を隠す
        maintenance_window = ctk.CTkToplevel(self.master)  # 新しいウィンドウを開く
        MaintenanceView(maintenance_window, self.on_maintenance_close)  # メンテナンス画面を表示

    def on_maintenance_close(self):
        """メンテナンス画面が閉じられたときの処理"""
        self.master.deiconify()  # メインウィンドウを再表示

def start_main_view():
    root = ctk.CTk()
    main_view = MainView(root)
    root.mainloop()
