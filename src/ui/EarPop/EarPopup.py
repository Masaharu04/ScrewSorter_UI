import customtkinter as ctk

class ErrorPopup:
    def __init__(self, master):
        self.master = master
        self.viewmodel = None  # ViewModelへの参照を保持するための変数を追加
        self.is_showing = False  # ポップアップ表示状態を管理する変数を追加
        self.error_codes = {
            "E001": "同じストッカーが選択されています。別のストッカーを選んでください。",
            "E002": "投入部のかき上げ機構が動作していない",
            "E003": "投入部のソレノイド異常（スライドシャッター）",
            "E004": "判別部のステッピングモーターの原点位置がずれている",
            "E005": "判別部のカメラ位置にボルトが存在しない",
            "E006": "判別部のボルトが適切に検出されなかった",
            "E007": "整列部の整列ラインにボルトがこない",
            "E008": "エクスポート時にUSBがささっていない",
            "E009": "画面の扉が開かれたまま",
            "E010": "投入部<->通信部 通信失敗",
            "E011": "判別部<->通信部 通信失敗",
            "E012": "整列部<->通信部 通信失敗",
            "E013": "通信部<->表示部 通信失敗",
            "E014": "投入部モーターとの通信失敗",
            "E015": "整列部モーターとの通信失敗",
            "E016": "判別部モーターとの通信失敗",
            "E017": "返却部モーターとの通信失敗",
            "E018": "投入部モーターの電流高くなる",
            "E019": "整列部モーターの電流高くなる",
            "E020": "判別部モーターの電流高くなる",
            "E021": "返却部モーターの電流高くなる",
            "E022": "投入部のかき上げが動いているか",
            "E023": "整列部ボルト残量の低下（A）",
            "E024": "整列部ボルト残量の低下（B）",
            "E025": "整列部ボルト残量の低下（C）",
            "E026": "整列部ボルト残量の低下（その他）",
            "E027": "投入部ボルト残量の低下"
        }

    def set_viewmodel(self, viewmodel):
        """ViewModelを設定するメソッド"""
        self.viewmodel = viewmodel

    def clear_error(self):
        """エラーをクリアしてポップアップを閉じる"""
        if self.viewmodel:
            print("エラーがクリアされました")  # エラークリア時にもメッセージを出力
            self.viewmodel.set_error_code(None)

    def show_error(self, error_code):
        # すでにポップアップが表示されている場合は新しいポップアップを表示しない
        if self.is_showing:
            return
            
        # エラーコードをターミナルに出力
        print(f"エラー発生: ERR_{error_code} - {self.error_codes.get(error_code, '不明なエラー')}")
        
        self.is_showing = True  # ポップアップ表示状態をTrueに設定
        
        # オーバーレイの作成
        overlay = ctk.CTkToplevel(self.master)
        overlay.overrideredirect(True)
        overlay.configure(fg_color='black')
        overlay.attributes('-alpha', 0.8)
        
        # メイン画面と同じ位置・サイズに設定
        overlay.geometry('800x480')
        overlay.geometry(f"+{self.master.winfo_x()}+{self.master.winfo_y()}")
        
        # エラーメッセージフレーム
        error_frame = ctk.CTkFrame(overlay, fg_color='black', corner_radius=10,
                                 width=500, height=350)
        error_frame.place(relx=0.5, rely=0.5, anchor="center")
        error_frame.pack_propagate(False)
        
        # エラーコードとメッセージの表示
        ctk.CTkLabel(error_frame, text=f"ERR_{error_code}", text_color="#FF0000",
                    font=("Arial", 28, "bold")).pack(pady=(30,20))
        
        error_message = self.error_codes.get(error_code, "不明なエラーが発生しました")
        
        # エラーメッセージの前に追加の説明文を表示
        explanation = ("以下の原因が考えられます。確認を行なってください。\n\n"
                      f"{error_message}")
        
        ctk.CTkLabel(error_frame, text=explanation, text_color="#FFFFFF",
                    font=("Arial", 16), justify="left").pack(padx=40, pady=(0,20))
        
        ctk.CTkLabel(error_frame, text=f"エラーコード：ERR_{error_code}",
                    text_color="#CCCCCC", font=("Arial", 14)).pack(pady=(0,20))
        
        # OKボタンの処理を変更
        def on_ok():
            self.is_showing = False  # ポップアップ表示状態をFalseに設定
            self.clear_error()  # エラーをクリア
            overlay.destroy()   # ポップアップを閉じる

        # OKボタン
        ctk.CTkButton(error_frame, text="OK", command=on_ok,
                     width=120, height=35, corner_radius=5).pack(pady=(0,30))