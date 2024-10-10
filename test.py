# ボタンフレームの設定
button_frame = ctk.CTkFrame(self.master, corner_radius=15)
button_frame.pack(padx=20, pady=20, fill="both")

# フレームのグリッドの行と列に重みを与えて中央配置を行う
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)
button_frame.grid_rowconfigure(0, weight=1)
button_frame.grid_rowconfigure(1, weight=1)

# ボタンの配置（行列レイアウトとサイズ調整）
for i, (text, color, command) in enumerate(buttons):
    button = ctk.CTkButton(button_frame, text=text, width=300, height=200, corner_radius=15, fg_color=color, command=command)
    button.grid(row=i // 3, column=i % 3, padx=40, pady=40)  # 大きめのパディングを設定
