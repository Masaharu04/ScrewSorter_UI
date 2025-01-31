import customtkinter as ctk
from ui.EarPop.EarPopup import ErrorPopup  # ErrorPopupをインポート
#from src.ui.stocker.stoker import create_stocker_frame


from datetime import datetime

class SettingViews:
    def __init__(self, master, on_close,callback_test, callback):
        self.master = master
        self.on_close = on_close
        self.callback_test = callback_test
        self.selected_labels = [None] * 3  # 選択されたラベルを保持するリスト
        self.error_popup = ErrorPopup(master)  # エラーポップアップのインスタンスを作成
        self.stocker_labels = ["ボルトM5(8mm)", "ボルトM5(10mm)", "ボルトM5(12mm)","ボルトM5(16mm)", 
                          "ボルトM6(8mm)", "ボルトM6(10mm)", "ボルトM6(12mm)", "ボルトM6(16mm)"] # ストッカーラベルをクラス属性として追加
        #self.selected_values = [0,0,0]  # 選択された値を保存するリストを追加
        self.setup_ui()
        self.callback = callback

    def setup_ui(self):
        # UIの各要素を順番にセットアップ
        self._setup_window()
        main_frame = self._create_main_frame()
        self._create_title(main_frame)
        self._create_stocker_selection(main_frame)  # ストッカー選択を追加
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
        title_label = ctk.CTkLabel(parent, text="設定画面", font=("Arial", 18))
        title_label.pack(pady=(0, 5))

    def _create_stocker_selection(self, parent):
        # ストッカー選択の作成
        stocker_labels = ["ボルトM5(8mm)", "ボルトM5(10mm)", "ボルトM5(12mm)","ボルトM5(16mm)", 
                          "ボルトM6(8mm)", "ボルトM6(10mm)", "ボルトM6(12mm)", "ボルトM6(16mm)"]
        
        # # 新しいボタンを追加
        # button_frame = ctk.CTkFrame(parent)  # ボタン用のフレームを作成
        # button_frame.pack(side="left", padx=10)  # 左側に配置
        
        # # ボタンを作成
        # TransitionSetting_button = ctk.CTkButton(button_frame, text="ボタン", command=self.open_timeSettingView,width=14, height=150)  # サンプルボタンを縦長に設定
        # TransitionSetting_button.pack(pady=1)

        for i in range(3):
            self.selected_labels[i] = ctk.StringVar(value=stocker_labels[0])
            label_frame = ctk.CTkFrame(parent)
            label_frame.pack(padx=20, pady=5)
            ctk.CTkLabel(label_frame, text=f"{chr(65 + i)}:").pack(side="left")  # A, B, Cのラベル
            
            for index, label in enumerate(stocker_labels):
                radio_button = ctk.CTkRadioButton(label_frame, text=label, variable=self.selected_labels[i], value=label, width=168, height=50)
                radio_button.pack(side="left", padx=5, pady=2)
                if (index + 1) % 4 == 0:
                    label_frame.pack()  # 新しい行を作成
                    label_frame = ctk.CTkFrame(parent)  # 新しいフレームを作成

    def _create_buttons(self, parent):
        # 下部のボタン（全停止と戻る）の作成
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill='x', pady=5)

        # 戻るボタン
        close_button = ctk.CTkButton(buttons_frame, text="戻る", command=self.close_setting_view,font=("Meiryo", 20, "bold"), width=200, height=60)
        close_button.pack(side='left',padx=(10, 10))

        # 選択したストッカーを表示するボタン
        confirm_button = ctk.CTkButton(buttons_frame, text="選択を確認", command=self.confirm_selection,font=("Meiryo", 20, "bold"), width=200, height=60)
        confirm_button.pack(side='left', padx=(10, 10))

    def confirm_selection(self):
        # 選択されたストッカーを表示
        self.selected_values = [self.stocker_labels.index(label.get()) for label in self.selected_labels]  # 選択された値を整数のインデックスで保存
        
        # 同じ項目が選ばれているかチェック
        if len(self.selected_values) != len(set(self.selected_values)):
            self.error_popup.show_error("E001")  # エラーコードを指定してポップアップを表示
            return
        #self.send_sirial()
        self.callback(self.selected_values)
        print(f"選択されたストッカー: {self.selected_values}")  # 保存した値を表示

    def close_setting_view(self):        
        self.master.destroy() 
    
    def send_sirial(self):

       # print(self.selected_values)
        new_array = []
        for value in self.selected_values:
            if value == 0:
                new_array.append(0b10101000)
            elif value == 1:
                new_array.append(0b10101010)
            elif value == 2:
                new_array.append(0b10101100)
            elif value == 3:
                new_array.append(0b10101111)
            elif value == 4:
                new_array.append(0b11001000)
            elif value == 5:
                new_array.append(0b11001010)
            elif value == 6:
                new_array.append(0b11001100)
            else:
                new_array.append(0b11001111)
        print(new_array)

        from src.base.views import MainView 
        main_view = MainView(self.master)
        main_view.send_stocker(new_array)

    # def open_timeSettingView(self):
    #     # サンプルボタンが押されたときの処理
    #     timesetting_window = ctk.CTkToplevel(self.master)
    #     TimeSettingView(timesetting_window,self.on_timesetting_close)
    #     print("時刻設定画面に遷移します")

    # def on_timesetting_close(self):
    #     self.master.destroy()


        

