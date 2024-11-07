import customtkinter as ctk

def shutdown_button_action():
    # シャットダウン確認ポップアップを表示
    show_shutdown_confirmation()

def show_shutdown_confirmation():
    # 確認ポップアップの作成
    overlay = ctk.CTkToplevel()
    overlay.overrideredirect(True)
    overlay.configure(fg_color='black')
    overlay.attributes('-alpha', 0.8)
    overlay.geometry('400x200')  # ポップアップのサイズ
    overlay.geometry(f"+{overlay.winfo_screenwidth()//2 - 200}+{overlay.winfo_screenheight()//2 - 100}")  # 中央に配置

    # 確認メッセージフレーム
    confirmation_frame = ctk.CTkFrame(overlay, fg_color='black', corner_radius=10)
    confirmation_frame.pack(padx=20, pady=20)

    # メッセージの表示
    ctk.CTkLabel(confirmation_frame, text="シャットダウンしてもいいですか？", 
                  text_color="#FFFFFF", font=("Arial", 16)).pack(pady=(20, 10))

    # ボタンの処理
    def on_confirm():
        print("シャットダウン処理を実行します")
        overlay.destroy()  # ポップアップを閉じる
        # ここに実際のシャットダウン処理を追加

    def on_cancel():
        overlay.destroy()  # ポップアップを閉じる

    # 確認ボタン
    ctk.CTkButton(confirmation_frame, text="はい", command=on_confirm, width=80).pack(side='left', padx=(0, 10), pady=(0, 20))
    # キャンセルボタン
    ctk.CTkButton(confirmation_frame, text="いいえ", command=on_cancel, width=80).pack(side='right', padx=(10, 0), pady=(0, 20))

# ... 既存のコード ...
