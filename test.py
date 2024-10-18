    # 各セクションを作成
    self.create_section(main_frame, "投入", "運転", "停止", "green", "red")
    self.create_section(main_frame, "判別", "運転", "停止", "green", "red")
    self.create_section(main_frame, "整列", "運転", "停止", "green", "red")
    self.create_section(main_frame, "返却", "運転", "停止", "green", "red")

def create_section(self, parent, title, start_text, stop_text, start_color, stop_color):
    section_frame = ctk.CTkFrame(parent)
    section_frame.pack(pady=10, padx=10, fill="x")  # フレームは横に広がるようにする

    title_label = ctk.CTkLabel(section_frame, text=title, font=("Arial", 18))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))  # タイトルは全体の上に配置

    start_button = ctk.CTkButton(section_frame, text=start_text, command=lambda: self.start_process(title), fg_color=start_color)
    start_button.grid(row=1, column=0, padx=(0, 10))  # ボタンを1行目の左に配置

    stop_button = ctk.CTkButton(section_frame, text=stop_text, command=lambda: self.stop_process(title), fg_color=stop_color)
    stop_button.grid(row=1, column=1)  # ボタンを1行目の右に配置
