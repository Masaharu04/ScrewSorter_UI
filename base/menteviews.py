import customtkinter as ctk

class MaintenanceView:
    def __init__(self, master, on_close):
        self.master = master
        self.on_close = on_close
        self.setup_ui()

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
        self.master.title("メンテナンス画面")
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

        self._input_section(sections_frame, "投入", 1, 1)
        self._discrimination_section(sections_frame, "判別", 1, 2)
        self._alignment_section(sections_frame, "整列", 1, 3)
        self._rebase_section(sections_frame, "返却", 1, 4)

    def _input_section(self, parent, title, row, col):
        # 各セクションの作成
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # タイトルラベル
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Meiryo", 30))
        title_label.pack(pady=(5, 5))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="運転", font=("Meiryo", 35, "bold"), command=lambda t=title: self.input_start(), width=160, height=110)
        start_button.pack(pady=(0, 15))
        
        # 停止ボタン
        stop_button = ctk.CTkButton(section_frame, text="停止",font=("Meiryo", 35, "bold"), command=lambda t=title: self.input_stop(),fg_color="red", width=160, height=110)
        stop_button.pack()
    def _discrimination_section(self, parent, title, row, col):
        # 各セクションの作成
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # タイトルラベル
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Meiryo", 30))
        title_label.pack(pady=(5, 5))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="運転",font=("Meiryo", 35, "bold"), command=lambda t=title: self.discrimination_start(), width=160, height=110)
        start_button.pack(pady=(0, 15))
        
        # 停止ボタン
        stop_button = ctk.CTkButton(section_frame, text="停止",font=("Meiryo", 35, "bold"), command=lambda t=title: self.discrimination_stop(),fg_color="red", width=160, height=110)
        stop_button.pack()
    def _alignment_section(self, parent, title, row, col):
        # 各セクションの作成
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # タイトルラベル
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Meiryo", 30))
        title_label.pack(pady=(5, 5))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="運転",font=("Meiryo", 35, "bold"), command=lambda t=title: self.alignment_start(), width=160, height=110)
        start_button.pack(pady=(0, 15))
        
        # 停止ボタン
        stop_button = ctk.CTkButton(section_frame, text="停止",font=("Meiryo", 35, "bold"), command=lambda t=title: self.alignment_stop(),fg_color="red", width=160, height=110)
        stop_button.pack()
    def _rebase_section(self, parent, title, row, col):
        # 各セクションの作成
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # タイトルラベル
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Meiryo", 30))
        title_label.pack(pady=(5, 5))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="運転",font=("Meiryo", 35, "bold"), command=lambda t=title: self.rebase_start(), width=160, height=110)
        start_button.pack(pady=(0, 15))
        
        # 停止ボタン
        stop_button = ctk.CTkButton(section_frame, text="停止",font=("Meiryo", 35, "bold"), command=lambda t=title: self.rebase_stop(), fg_color="red", width=160, height=110)
        stop_button.pack()

    def _create_buttons(self, parent):
        # 下部のボタン（全停止と戻る）の作成
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill='x', pady=5)

        # 戻るボタン
        close_button = ctk.CTkButton(buttons_frame, text="戻る", command=self.close_maintenance_view, font=("Meiryo", 20, "bold"),width=200, height=70)
        close_button.pack(side='left', padx=(10, 10),pady=(10, 10))

        # 全停止ボタン
        stop_button = ctk.CTkButton(buttons_frame, text="全停止", command=self.master_stop, font=("Meiryo", 20, "bold"), fg_color="red", width=200, height=70)
        stop_button.pack(side='left', padx=(0, 10),pady=(10, 10))


    def stop_all(self):
        print("全停止します")

    def close_maintenance_view(self):
        self.master.destroy()
        self.on_close()

    def input_start(self):
        from src.base.views import MainView 
        main_view = MainView(self.master)
        main_view.send_input_start()
        
    def input_stop(self):
        from src.base.views import MainView 
        main_view = MainView(self.master)
        main_view.send_input_stop()

    def discrimination_start(self):
        from src.base.views import MainView 
        main_view = MainView(self.master)
        main_view.send_discrimination_start()

    def discrimination_stop(self):
        from src.base.views import MainView 
        main_view = MainView(self.master)
        main_view.send_discrimination_stop()

    def alignment_start(self):
        from src.base.views import MainView 
        main_view = MainView(self.master)
        main_view.send_discrimination_start()

    def alignment_stop(self):
        from src.base.views import MainView 
        main_view = MainView(self.master)
        main_view.send_discrimination_stop()

    def rebase_start(self):
        from src.base.views import MainView 
        main_view = MainView(self.master)
        main_view.send_discrimination_start()

    def rebase_stop(self):
        from src.base.views import MainView 
        main_view = MainView(self.master)
        main_view.send_discrimination_stop()

    def master_stop(self):
        from src.base.views import MainView
        main_view = MainView(self.master)
        main_view.mastr_stop(self.master)

        