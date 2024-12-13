import customtkinter as ctk
from src.ui.EarPop.EarPopup import ErrorPopup  # ErrorPopupをインポート
from src.ui.stocker.stoker import create_stocker_frame

class MaintenanceView:
    def __init__(self, master, on_close,callback_test):
        self.master = master
        self.on_close = on_close
        self.callback_test = callback_test
        self.selected_labels = [None] * 3  # 選択されたラベルを保持するリスト
        self.error_popup = ErrorPopup(master)  # エラーポップアップのインスタンスを作成
        self.stocker_labels = ["ボルトM4(5mm)", "ボルトM4(6mm)", "ボルトM4(8mm)"]  # ストッカーラベルをクラス属性として追加
        self.selected_values = []  # 選択された値を保存するリストを追加
        self.setup_ui()

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
        stocker_labels = ["ボルトM4(5mm)", "ボルトM4(6mm)", "ボルトM4(8mm)"]
        
        for i in range(3):
            self.selected_labels[i] = ctk.StringVar(value=stocker_labels[0])
            label_frame = ctk.CTkFrame(parent)
            label_frame.pack(anchor="w", padx=20, pady=5)
            ctk.CTkLabel(label_frame, text=f"{chr(65 + i)}:").pack(side="left")  # A, B, Cのラベル
            
            for label in stocker_labels:
                radio_button = ctk.CTkRadioButton(label_frame, text=label, variable=self.selected_labels[i], value=label)
                radio_button.pack(side="left", padx=5)

    def _create_buttons(self, parent):
        # 下部のボタン（全停止と戻る）の作成
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill='x', pady=5)

        # 戻るボタン
        close_button = ctk.CTkButton(buttons_frame, text="戻る", command=self.close_maintenance_view, width=100, height=30)
        close_button.pack(side='left')

        # 選択したストッカーを表示するボタン
        confirm_button = ctk.CTkButton(buttons_frame, text="選択を確認", command=self.confirm_selection, width=100, height=30)
        confirm_button.pack(side='left', padx=(10, 0))

    def confirm_selection(self):
        # 選択されたストッカーを表示
        self.selected_values = [self.stocker_labels.index(label.get()) for label in self.selected_labels]  # 選択された値を整数のインデックスで保存
        
        # 同じ項目が選ばれているかチェック
        if len(self.selected_values) != len(set(self.selected_values)):
            self.error_popup.show_error("E001")  # エラーコードを指定してポップアップを表示
            return
        
        print(f"選択されたストッカー: {self.selected_values}")  # 保存した値を表示

    def close_maintenance_view(self):
        self.callback_test(1)
        self.master.destroy() 
        print(self.selected_values)
        return self.selected_values
