import customtkinter as ctk

class ShutdownPopup:
    def __init__(self, master):
        self.master = master
        self.is_showing = False 

    def shutdown_button_action(self):
        # シャットダウン確認ポップアップを表示
        if self.is_showing:
            return
        self.is_showing = True
        self.show_shutdown_confirmation()

    def show_shutdown_confirmation(self):
        # 確認ポップアップの作成
        overlay = ctk.CTkToplevel(self.master)
        overlay.overrideredirect(True)
        overlay.configure(fg_color='black')
        overlay.attributes('-alpha', 1.8)
        overlay.geometry('400x200')
        overlay.geometry(f"+{self.master.winfo_screenwidth()//2 - 200}+{self.master.winfo_screenheight()//2 - 100}")  # 画面の中央に配置

        # エラーメッセージフレーム
        confirmation_frame = ctk.CTkFrame(overlay, fg_color='black', corner_radius=10, width=400, height=200)
        confirmation_frame.pack_propagate(False)
        confirmation_frame.pack(pady=(20, 20), padx=(20, 20))

        # メッセージラベル
        message_label = ctk.CTkLabel(confirmation_frame, text="シャットダウンしてもいいですか？", font=("Arial", 16), text_color="#FFFFFF")
        message_label.pack(pady=(20, 10))

        # OKボタン
        ok_button = ctk.CTkButton(confirmation_frame, text="OK", command=self.shutdown_action)
        ok_button.pack(side='left', padx=(50, 10), pady=(10, 20))

        # キャンセルボタン
        cancel_button = ctk.CTkButton(confirmation_frame, text="キャンセル", command=lambda: self.close_popup(overlay))
        cancel_button.pack(side='right', padx=(10, 50), pady=(10, 20))

    def shutdown_action(self):
        print("シャットダウン処理を実行します")
        # ここに実際のシャットダウン処理を追加
     
       
    def close_popup(self, overlay):
        self.is_showing = False  
        overlay.destroy()  
