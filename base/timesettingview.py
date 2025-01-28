import customtkinter as ctk

class TimeSettingView:
    def __init__(self, master, on_close):
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        # UIの各要素を順番にセットアップ
        self._setup_window()
        main_frame = self._create_main_frame()
        self._create_title(main_frame)

    def _setup_window(self):
        # ウィンドウの基本設定
        self.master.title("メンテナンス画面")
        self.master.geometry('800x480')
        self.master.overrideredirect(True)  # タイトルバーを非表示

    def _create_main_frame(self):
        # メインフレームの作成
        main_frame = ctk.CTkFrame(self.master)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        return main_frame

    