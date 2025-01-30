import customtkinter as ctk

class TimeSettingView:
    def __init__(self, master, on_close):
        self.master = master
        self.on_close = on_close
        self.setup_ui()

    def setup_ui(self):
        # UIの各要素を順番にセットアップ
        self._setup_window()
        main_frame = self._create_main_frame()
        self._create_time_setting_widgets(main_frame)  # 時刻設定用のウィジェットを追加
        self._create_return_button(main_frame)  # 戻るボタンを追加

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

    def _create_time_setting_widgets(self, parent):
        # 時刻設定用のウィジェットを作成
        time_frame = ctk.CTkFrame(parent)
        time_frame.pack(expand=True, fill='both', pady=20)



    def _create_time_widget(self, parent, var, label_text, max_value):
        # 時間ウィジェットの作成
        widget_frame = ctk.CTkFrame(parent)
        widget_frame.pack(side='left', padx=15, pady=5)

        label = ctk.CTkLabel(widget_frame, text=label_text)
        label.pack()

        up_button = ctk.CTkButton(widget_frame, text="▲", command=lambda: self._increment_time(var, max_value), width=30)
        up_button.pack()

        display = ctk.CTkLabel(widget_frame, textvariable=var, width=30)
        display.pack()

        down_button = ctk.CTkButton(widget_frame, text="▼", command=lambda: self._decrement_time(var, max_value), width=30)
        down_button.pack()

    def _create_return_button(self, parent):
        # 戻るボタンの作成
        return_button = ctk.CTkButton(parent, text="戻る", command=self.timesetting_close)
        return_button.pack(side='bottom', pady=10)

    def timesetting_close(self):        
        self.master.destroy() 