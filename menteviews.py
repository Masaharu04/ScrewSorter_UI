import customtkinter as ctk

class MaintenanceView:
    def __init__(self, master, on_close):
        self.master = master
        self.on_close = on_close  # メインウィンドウを再表示するためのコールバック
        self.setup_ui()

    def setup_ui(self):
        self.master.title("メンテナンス画面")
        # ウィンドウサイズを800x400に設定
        self.master.geometry('800x400')

        #self.master.attributes('-fullscreen', True)  # フルスクリーン設定（必要に応じて有効化）
        self.master.overrideredirect(True)  # ウィンドウのバーを非表示

        # メインフレームを作成
        main_frame = ctk.CTkFrame(self.master)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)  # パディングを少し狭める

        # タイトルラベル
        title_label = ctk.CTkLabel(main_frame, text="メンテナンス画面", font=("Arial", 20))  # フォントサイズを少し小さめに
        title_label.pack(pady=(0, 10))  # 上部の余白を少し縮小

        # 各セクションを作成（セクションごとの余白を調整）
        self.create_section(main_frame, "投入", "運転", "停止", "green", "red")
        self.create_section(main_frame, "判別", "運転", "停止", "green", "red")
        self.create_section(main_frame, "整列", "運転", "停止", "green", "red")
        self.create_section(main_frame, "返却", "運転", "停止", "green", "red")

        # 全停止ボタン
        stop_button = ctk.CTkButton(main_frame, text="全停止", command=self.stop_all, fg_color="red")
        stop_button.pack(pady=(10, 5))  # パディングを少し狭める

        # 戻るボタン
        close_button = ctk.CTkButton(main_frame, text="戻る", command=self.close_maintenance_view)
        close_button.pack(pady=(5, 10))  # パディングを調整

        # setup_frameの作成（均等配置のための調整）
        setup_frame = ctk.CTkFrame(self.master)
        setup_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # 各列に均等に余白を与え、中央に配置するための grid 設定
        setup_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # 全停止ボタンを横一列に並べる
        for i in range(5):
            stop_button = ctk.CTkButton(setup_frame, text=f"全停止 {i+1}", command=self.stop_all, fg_color="red")
            stop_button.grid(row=0, column=i, padx=5, pady=5)  # パディングを少し狭める

    def create_section(self, parent, title, start_text, stop_text, start_color, stop_color):
        # 各セクションのフレームを作成し、パディングを最適化
        section_frame = ctk.CTkFrame(parent)
        section_frame.pack(pady=5)  # セクションごとの上下の余白を小さく

        title_label = ctk.CTkLabel(section_frame, text=title, font=("Arial", 16))  # フォントサイズを少し小さめに
        title_label.pack(pady=(0, 5))  # タイトルラベルの下部余白を少し狭める

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text=start_text, command=lambda: self.start_process(title), fg_color=start_color)
        start_button.pack(side='left', padx=(0, 5))  # ボタンの横余白を縮小

        # 停止ボタン
        stop_button = ctk.CTkButton(section_frame, text=stop_text, command=lambda: self.stop_process(title), fg_color=stop_color)
        stop_button.pack(side='left')

    def start_process(self, title):
        print(f"{title}を運転します")

    def stop_process(self, title):
        print(f"{title}を停止します")

    def stop_all(self):
        print("全停止します")

    def close_maintenance_view(self):
        self.master.destroy()  # メンテナンス画面を閉じる
        self.on_close()  # メインウィンドウを再表示するためのコールバックを呼び出す
