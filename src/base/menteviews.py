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
        title_label = ctk.CTkLabel(parent, text="メンテナンス画面", font=("Arial", 18))
        title_label.pack(pady=(0, 5))

    def _create_sections(self, parent):
        # 4つのセクションを含むフレームの作成
        sections_frame = ctk.CTkFrame(parent)
        sections_frame.pack(expand=True, fill='both', pady=5)

        # 4つのセクションを2x2グリッドで配置
        for i, title in enumerate(["投入", "判別", "整列", "返却"]):
            row, col = divmod(i, 2)
            self._create_section(sections_frame, title, row, col)

    def _create_section(self, parent, title, row, col):
        # 各セクションの作成
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

        # タイトルラベル
        title_label = ctk.CTkLabel(section_frame, text=title)
        title_label.pack(pady=(0, 5))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="運転", command=lambda t=title: self.start_process(t), width=160, height=60)
        start_button.pack(pady=(0, 5))

        # 停止ボタン
        stop_button = ctk.CTkButton(section_frame, text="停止", command=lambda t=title: self.stop_process(t), width=160, height=60)
        stop_button.pack()

    def _create_buttons(self, parent):
        # 下部のボタン（全停止と戻る）の作成
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill='x', pady=5)

        # 全停止ボタン
        stop_button = ctk.CTkButton(buttons_frame, text="全停止", command=self.stop_all, fg_color="red", width=160, height=60)
        stop_button.pack(side='left', padx=(0, 5))

        # 戻るボタン
        close_button = ctk.CTkButton(buttons_frame, text="戻る", command=self.close_maintenance_view, width=160, height=60)
        close_button.pack(side='left')

    def start_process(self, title):
        print(f"{title}を運転します")

    def stop_process(self, title):
        print(f"{title}を停止します")

    def stop_all(self):
        print("全停止します")

    def close_maintenance_view(self):
        self.master.destroy()
        self.on_close()
