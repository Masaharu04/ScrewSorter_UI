import customtkinter as ctk
from send_data import SendModuleOperation, SendPatrolLampStateChange
class MaintenanceView:
    def __init__(self, master, on_close):
        self.master = master
        self.on_close = on_close
        self.send_module_operation = SendModuleOperation()
        self.send_potrol_lamp = SendPatrolLampStateChange()
        self.setup_ui()
        self.button_states = {}

        # カーソルを非表示にする
        self.master.config(cursor="")

    def setup_ui(self):
        # UIの各要素を順番にセットアップ
        self._setup_window()
        main_frame = self._create_main_frame()
        self._create_title(main_frame)
        self._create_sections(main_frame)
        self._create_buttons(main_frame)

    def _setup_window(self):
        # ウィンドウの基本設定
        self.master.title("モジュール個別操作画面")
        self.master.geometry('800x480')
        self.master.overrideredirect(True)  # タイトルバーを非表示

    def _create_main_frame(self):
        # メインフレームの作成
        main_frame = ctk.CTkFrame(self.master)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        return main_frame

    def _create_title(self, parent):
        # タイトルラベルの作成
        title_label = ctk.CTkLabel(parent, text="メンテナンス画面", font=("Arial", 20, "bold"))
        title_label.pack(pady=(7, 5))

    def _create_sections(self, parent):
        # 4つのセクションを含むフレームの作成
        sections_frame = ctk.CTkFrame(parent)
        sections_frame.pack(expand=True, fill='both', pady=5)

        self._input_section(sections_frame, "投入部", 1, 1)
        self._discrimination_section(sections_frame, "判別部", 1, 2)
        self._alignment_section(sections_frame, "整列部", 1, 3)
        self._rebase_section(sections_frame, "返却部", 1, 4)
        self._back_section(sections_frame, "戻る", 1, 5)

    def _back_section(self, parent, title, row, col):
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="戻る", font=("Meiryo", 35, "bold"), command=lambda t=title: self.close_maintenance_view(), width=20, height=280)
        start_button.pack(pady=(0, 0))


    def _input_section(self, parent, title, row, col):
        # 各セクションの作成
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # タイトルラベル
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Meiryo", 30))
        title_label.pack(pady=(5, 5))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="運転", font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button, lambda: self.input_start()), width=150, height=110)
        start_button.pack(pady=(0, 15))
        
        # 停止ボタン
        stop_button = ctk.CTkButton(section_frame, text="停止",font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(stop_button, lambda: self.input_stop()),fg_color="red", width=150, height=110)
        stop_button.pack()
    def _discrimination_section(self, parent, title, row, col):
        # 各セクションの作成
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # タイトルラベル
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Meiryo", 30))
        title_label.pack(pady=(5, 5))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="運転",font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button, lambda: self.discrimination_start()), width=150, height=110)
        start_button.pack(pady=(0, 15))
        
        # 停止ボタン
        stop_button = ctk.CTkButton(section_frame, text="停止",font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(stop_button, lambda: self.discrimination_stop()),fg_color="red", width=150, height=110)
        stop_button.pack()
    def _alignment_section(self, parent, title, row, col):
        # 各セクションの作成
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # タイトルラベル
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Meiryo", 30))
        title_label.pack(pady=(5, 5))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="運転",font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button, lambda: self.alignment_start()), width=150, height=110)
        start_button.pack(pady=(0, 15))
        
        # 停止ボタン
        stop_button = ctk.CTkButton(section_frame, text="停止",font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(stop_button, lambda: self.alignment_stop()),fg_color="red", width=150, height=110)
        stop_button.pack()
    def _rebase_section(self, parent, title, row, col):
        # 各セクションの作成
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # タイトルラベル
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Meiryo", 30))
        title_label.pack(pady=(5, 5))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="運転",font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button, lambda: self.rebase_start()), width=150, height=110)
        start_button.pack(pady=(0, 15))
        
        # 停止ボタン
        stop_button = ctk.CTkButton(section_frame, text="停止",font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(stop_button, lambda: self.rebase_stop()), fg_color="red", width=150, height=110)
        stop_button.pack()

    def _create_buttons(self, parent):
        # 下部のボタン（全停止と戻る）の作成
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill='x', pady=5)

        # 全停止ボタン
        stop_button = ctk.CTkButton(buttons_frame, text="全停止", command=lambda: self.handle_button_click(stop_button, lambda: self.master_stop()), font=("Meiryo", 20, "bold"), fg_color="red", width=780, height=70)
        stop_button.pack(side='left', padx=(0, 10),pady=(10, 10))


    def stop_all(self):
        print("全停止します")

    def close_maintenance_view(self):

        self.on_close()
        self.master.destroy()

    def input_start(self):
        self.send_module_operation.send_input_module_start()
        print("send_input_module_start")
        
    def input_stop(self):
        self.send_module_operation.send_input_module_stop()
        print("send_input_module_stop")

    def discrimination_start(self):
       self.send_module_operation.send_discrimination_module_start()
       print("send_discrimination_module_start")

    def discrimination_stop(self):
        self.send_module_operation.send_discrimination_module_stop()
        print("send_discrimination_module_stop")

    def alignment_start(self):
        self.send_module_operation.send_alignment_module_start()
        print("send_return_module_start")

    def alignment_stop(self):
        self.send_module_operation.send_alignment_module_stop()
        print("send_return_module_stop")

    def rebase_start(self):
        self.send_module_operation.send_return_module_start()
        print("send_alignment_module_start")

    def rebase_stop(self):
        self.send_module_operation.send_return_module_stop()
        print("send_alignment_module_stop")

    def master_stop(self):
        self.input_stop()
        self.discrimination_stop()
        self.alignment_stop()
        self.rebase_stop()
        print("send_all_module_stop")
        

    def handle_button_click(self, button, callback):
        """ボタンクリックを処理し、チャタリング防止を実装する"""
        if button not in self.button_states or not self.button_states.get(button):
            # ボタンを無効化
            self.button_states[button] = True
            button.configure(state="disabled")
            
            # コールバック実行
            callback()
            # self.show_popup()
            # 1秒後にボタンを再度有効化
            self.master.after(2000, lambda: self.enable_button(button))
            

    def enable_button(self, button):
        """ボタンを再度有効化する"""
        self.button_states[button] = False
        button.configure(state="normal")
