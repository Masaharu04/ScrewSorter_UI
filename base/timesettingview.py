import customtkinter as ctk
from datetime import datetime
#from Rtc import RtcControl

class TimeSettingView:
    def __init__(self, master, on_close):
        self.master = master
        self.on_close = on_close
        self.setup_ui()

    def setup_ui(self):
        self._setup_window()
        main_frame = self._create_main_frame()
        self._create_time_setting_widgets(main_frame)
        self._create_buttons(main_frame)

    def _setup_window(self):
        self.master.title("メンテナンス画面")
        self.master.geometry('800x480')
        self.master.overrideredirect(True)

    def _create_main_frame(self):
        main_frame = ctk.CTkFrame(self.master)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        return main_frame

    def _create_time_setting_widgets(self, parent):
        time_frame = ctk.CTkFrame(parent)
        time_frame.pack(expand=True, fill='both', pady=20)
        
        now = datetime.now()
        self.year = ctk.IntVar(value=now.year)
        self.month = ctk.IntVar(value=now.month)
        self.day = ctk.IntVar(value=now.day)
        self.hour = ctk.IntVar(value=now.hour)
        self.minute = ctk.IntVar(value=now.minute)
        
        self._create_time_widget(time_frame, self.year, "年", range(2000, 2100))
        self._create_time_widget(time_frame, self.month, "月", range(1, 13))
        self._create_time_widget(time_frame, self.day, "日", range(1, 32))
        self._create_time_widget(time_frame, self.hour, "時", range(0, 24))
        self._create_time_widget(time_frame, self.minute, "分", range(0, 60))
    
    def _create_time_widget(self, parent, var, label_text, value_range):
        widget_frame = ctk.CTkFrame(parent)
        widget_frame.pack(side='left', padx=25, pady=20)
        
        label = ctk.CTkLabel(widget_frame, text=label_text, font=("Arial", 32))
        label.pack()
        
        up_button = ctk.CTkButton(widget_frame, text="▲", command=lambda: self._increment_time(var, value_range), width=80, height=80)
        up_button.pack()
        
        display = ctk.CTkLabel(widget_frame, textvariable=var, width=80, font=("Arial", 32))
        display.pack()
        
        down_button = ctk.CTkButton(widget_frame, text="▼", command=lambda: self._decrement_time(var, value_range), width=80, height=80)
        down_button.pack()
    
    def _increment_time(self, var, value_range):
        current = var.get()
        next_value = current + 1
        if next_value in value_range:
            var.set(next_value)

    def _decrement_time(self, var, value_range):
        current = var.get()
        next_value = current - 1
        if next_value in value_range:
            var.set(next_value)
    
    def save_settings(self):
        
        print(f"設定されたRTC時刻: {self.year.get()}/{self.month.get()}/{self.day.get()} {self.hour.get()}:{self.minute.get()}")
        # RTC 設定用のコードをここに追加
        # self.rtc_control.set_date(f"{self.year.get()}/{self.month.get()}/{self.day.get()}/{self.hour.get()}/{self.minute.get()}")
        self.master.destroy()

    def _create_buttons(self, parent):
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(side='bottom', pady=20)
        
        save_button = ctk.CTkButton(button_frame, text="設定を保存", command=self.save_settings, height=80, width=300, font=("Arial", 24))
        save_button.pack(side='left', padx=20)
        
        # return_button = ctk.CTkButton(button_frame, text="戻る", command=self.timesetting_close, height=80, width=300, font=("Arial", 24))
        # return_button.pack(side='right', padx=20)

    def timesetting_close(self):        
        self.master.destroy()
