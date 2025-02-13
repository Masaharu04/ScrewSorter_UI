import customtkinter as ctk
from send_data import SendSolenoidIndividualOperation
class SorenoidMenteView:
    def __init__(self, master, on_close):
        self.master = master
        self.on_setting_close = on_close
        self.send_solenoidindividual_operation = SendSolenoidIndividualOperation()
        self.setup_ui()
        self.button_states = {}
        # カーソルを非表示にする
        self.master.config(cursor="")

    def setup_ui(self):
        # UIの各要素を順番にセットアップ
        self._setup_window()
        main_frame = self._create_main_frame()
        self._create_title(main_frame)
        self._create_sections(main_frame)
    

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
        title_label = ctk.CTkLabel(parent, text="ソレノイド個別操作画面", font=("Arial", 20, "bold"))
        title_label.pack(pady=(7, 5))

    def _create_sections(self, parent):
        # 4つのセクションを含むフレームの作成
        sections_frame = ctk.CTkFrame(parent)
        sections_frame.pack(expand=True, fill='both', pady=5)
        self._back_section(sections_frame, "戻る", 1, 1)
        self._sorenoid_A_section(sections_frame, "投入部", 1, 2)
        self._sorenoid_B_section(sections_frame, "判別部", 1, 3)
        self._sorenoid_C_section(sections_frame, "整列部", 1, 4)
        
    def _back_section(self, parent, title, row, col):
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="戻る", font=("Meiryo", 35, "bold"), command=lambda t=title: self.close_maintenance_view(), width=20, height=280)
        start_button.pack(pady=(45, 0))


    def _sorenoid_A_section(self, parent, title, row, col):
        # 各セクションの作成
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # タイトルラベル
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Meiryo", 30))
        title_label.pack(pady=(5, 5))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="シャッター", font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button,lambda: self.sore1()), width=200, height=50)
        start_button.pack(pady=(0, 15))
  
    def _sorenoid_B_section(self, parent, title, row, col):
        # 各セクションの作成
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # タイトルラベル
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Meiryo", 30))
        title_label.pack(pady=(5, 5))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="タイプA", font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button, lambda: self.sore2()), width=200, height=50)
        start_button.pack(pady=(0, 15))
        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="タイプB", font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button, lambda: self.sore3()), width=200, height=50)
        start_button.pack(pady=(0, 15))
        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="タイプC", font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button, lambda: self.sore4()), width=200, height=50)
        start_button.pack(pady=(0, 15))
        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="その他", font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button, lambda: self.sore5()), width=200, height=50)
        start_button.pack(pady=(0, 15))
        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="返却", font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button, lambda: self.sore6()), width=200, height=50)
        start_button.pack(pady=(0, 15))

    def _sorenoid_C_section(self, parent, title, row, col):
        # 各セクションの作成
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # タイトルラベル
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Meiryo", 30))
        title_label.pack(pady=(5, 5))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="タイプA", font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button, lambda: self.sore7()), width=200, height=50)
        start_button.pack(pady=(0, 15))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="タイプB", font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button, lambda: self.sore8()), width=200, height=50)
        start_button.pack(pady=(0, 15))

        # 運転ボタン
        start_button = ctk.CTkButton(section_frame, text="タイプC", font=("Meiryo", 35, "bold"), command=lambda t=title: self.handle_button_click(start_button, lambda: self.sore9()), width=200, height=50)
        start_button.pack(pady=(0, 15))

    def sore1(self):
        self.send_solenoidindividual_operation.operate_shutter_solenoid_in_input()
        print("operate_shutter_solenoid_in_input")
    def sore2(self):
        self.send_solenoidindividual_operation.operate_solenoid_a_in_discrimination()
        print("operate_solenoid_a_in_discrimination")
    def sore3(self):
        self.send_solenoidindividual_operation.operate_solenoid_b_in_discrimination()
        print("operate_solenoid_b_in_discrimination")
    def sore4(self):
        self.send_solenoidindividual_operation.operate_solenoid_c_in_discrimination()
        print("operate_solenoid_c_in_discrimination")
    def sore5(self):
        self.send_solenoidindividual_operation.operate_solenoid_etc_in_discrimination()
        print("operate_solenoid_etc_in_discrimination")
    def sore6(self):
        self.send_solenoidindividual_operation.operate_solenoid_return_in_discrimination()
        print("operate_solenoid_return_in_discrimination")
    def sore7(self):
        self.send_solenoidindividual_operation.operate_solenoid_a_in_alignment()
        print("operate_solenoid_a_in_alignment")
    def sore8(self):
        self.send_solenoidindividual_operation.operate_solenoid_b_in_alignment()
        print("operate_solenoid_b_in_alignment")
    def sore9(self):
        self.send_solenoidindividual_operation.operate_solenoid_c_in_alignment()
        print("operate_solenoid_c_in_alignment")


    def close_maintenance_view(self):
        self.on_setting_close()
        self.master.destroy()
        
    def handle_button_click(self, button, callback):
        """ボタンクリックを処理し、チャタリング防止を実装する"""
        if button not in self.button_states or not self.button_states.get(button):
            # ボタンを無効化
            self.button_states[button] = True
            button.configure(state="disabled")
            
            # コールバック実行
            callback()
            # self.show_popup()
            # 1秒後にボタンを再度有効化
            self.master.after(2000, lambda: self.enable_button(button))
            

    def enable_button(self, button):
        """ボタンを再度有効化する"""
        self.button_states[button] = False
        button.configure(state="normal")
