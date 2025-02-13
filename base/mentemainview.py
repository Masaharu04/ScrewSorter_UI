import customtkinter as ctk
from base.menteviews import MaintenanceView
from base.mentesorenoido import SorenoidMenteView
from send_data import SendMotorManualOperation , SendMotorReset,SendConfigurationChange, SendPatrolLampStateChange
class MaintenanceMainView:
    def __init__(self, master, on_close, motervalue):
        self.master = master
        self.on_close = on_close
        self.motervalue = motervalue
        
        # ボタンの状態を管理する変数を追加
        self.button_states = {}
        
        self.send_motormanual_operation = SendMotorManualOperation()
        self.send_motor_reset = SendMotorReset()
        self.send_configuration_change = SendConfigurationChange()
        self.send_potrol_lamp = SendPatrolLampStateChange()
        # カスタムカラーの定義
        self.colors = {
            "background": "#1E1E1E",    # ダークモード背景
            "button": "#1F6AA5",        # モダンなブルー
            "button_hover": "#2563EB",   # ホバー時の濃いブルー
            "danger": "#FF0000",        # 警告用レッド
            "text": "#FFFFFF",          # テキスト色
            "panel": "#2D2D2D"          # パネル背景
        }
        
        self.values = self.motervalue#[4, 4, 4]  # 数値制御の初期値
        
        self.setup_ui()
        self.master.config(cursor="")

    def setup_ui(self):
        self._setup_window()
        self._create_layout()

    def _setup_window(self):
        self.master.title("メンテナンス画面")
        self.master.geometry('800x480')
        self.master.overrideredirect(True)
        self.master.configure(bg=self.colors["background"])

    def _create_layout(self):
        # メインコンテナ
        # メインコンテナをさらにまとめるフレーム
        main_frame = ctk.CTkFrame(self.master, fg_color=self.colors["background"], width=800, height=480)
        main_frame.pack(padx=10, pady=10)

        # 左側の画面移動用ボタン
        left_button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")  # masterフレームに直接配置
        left_button_frame.pack(side='left', padx=10)
        
        ctk.CTkButton(
            left_button_frame,
            text="←",
            width=60,
            height=260,
            fg_color=self.colors["button"],
            hover_color=self.colors["button_hover"],
            font=("Arial", 18, "bold"),
            command=lambda: self.moveview()
        ).pack(pady=0)

        # 右側の画面移動用ボタン
        right_button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")  # masterフレームに直接配置
        right_button_frame.pack(side='right', padx=10)
        
        ctk.CTkButton(
            right_button_frame,
            text="→",
            width=60,
            height=260,
            fg_color=self.colors["button"],
            hover_color=self.colors["button_hover"],
            font=("Arial", 18, "bold"),
            command=lambda: self.sorenoid_view()
        ).pack(pady=10)

        # メインコンテナ
        container = ctk.CTkFrame(main_frame, fg_color=self.colors["background"])
        container.pack(expand=True, fill='both', padx=0, pady=20)

        # 上部パネル - 制御ボタン用
        top_panel = ctk.CTkFrame(container, fg_color=self.colors["panel"], corner_radius=15)
        top_panel.pack(fill='x', expand=False, padx=0, pady=(0, 10))

        # 制御ボタングリッド
        for i in range(3):
            control_frame = ctk.CTkFrame(top_panel, fg_color="transparent")
            control_frame.pack(side='left', expand=False, padx=5, pady=15)
            
            labels = ["投入部モータ動作", "判別部モータ動作", "返却部モータ動作"]
            ctk.CTkLabel(control_frame, text=labels[i], font=("Arial", 16)).pack()
            
            button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
            button_frame.pack(pady=5)
            
            if i == 0:
                button_on = ctk.CTkButton(
                    button_frame,
                    text="ON",
                    width=90,
                    height=50,
                    fg_color=self.colors["button"],
                    hover_color=self.colors["button_hover"],
                    font=("Arial", 16, "bold"),
                    command=lambda: self.handle_button_click(
                        button_on,
                        lambda: self.send_motormanual_operation.send_input_manual_start()
                    )
                ).pack(side='left', padx=5)
                
                button_off = ctk.CTkButton(
                    button_frame,
                    text="OFF", 
                    width=90,
                    height=50,
                    fg_color=self.colors["danger"],
                    hover_color="#DC2626",
                    font=("Arial", 16, "bold"),
                    command=lambda: self.handle_button_click(
                        button_off,
                        lambda: self.send_motormanual_operation.send_input_manual_stop()
                    )
                )
                button_off.pack(side='left', padx=5)

            elif i == 1:
                button_on = ctk.CTkButton(
                    button_frame,
                    text="ON",
                    width=90,
                    height=50,
                    fg_color=self.colors["button"],
                    hover_color=self.colors["button_hover"],
                    font=("Arial", 16, "bold"),
                    command=lambda: self.handle_button_click(
                        button_on,
                        lambda: self.send_motormanual_operation.send_discrimination_manual_start()
                    )        
                )
                button_on.pack(side='left', padx=5)
                
                button_off = ctk.CTkButton(
                    button_frame,
                    text="OFF",
                    width=90,
                    height=50,
                    fg_color=self.colors["danger"],
                    hover_color="#DC2626",
                    font=("Arial", 16, "bold"),
                    command=lambda: self.handle_button_click(
                        button_off,
                        lambda: self.send_motormanual_operation.send_discrimination_manual_stop()
                    )
                )
                button_off.pack(side='left', padx=5)
            else:
                button_on = ctk.CTkButton(
                    button_frame,
                    text="ON",
                    width=90,
                    height=50,
                    fg_color=self.colors["button"],
                    hover_color=self.colors["button_hover"],
                    font=("Arial", 16, "bold"),
                    command=lambda: self.handle_button_click(
                        button_on,
                        lambda: self.send_motormanual_operation.send_return_manual_start()
                    )
                )
                button_on.pack(side='left', padx=5)
                
                button_off = ctk.CTkButton(
                    button_frame,
                    text="OFF",
                    width=90,
                    height=50,
                    fg_color=self.colors["danger"],
                    hover_color="#DC2626",
                    font=("Arial", 16, "bold"),
                    command=lambda: self.handle_button_click(
                        button_off,
                        lambda: self.send_motormanual_operation.send_return_manual_stop()
                    )
                )
                button_off.pack(side='left', padx=5)

        # 中央パネル
        center_panel = ctk.CTkFrame(container, fg_color=self.colors["panel"], corner_radius=15)
        center_panel.pack(side='left', expand=True, fill='both', pady=0, padx=0)  # 左に寄せるためにside='left'を追加

        # 左側：STEPボタン
        step_frame = ctk.CTkFrame(center_panel, fg_color="transparent")
        step_frame.pack(side='left', padx=20)
        
        ctk.CTkLabel(step_frame, text="45度ステップ動作", font=("Arial", 16)).pack(pady=5)
        step_button = ctk.CTkButton(
            step_frame,
            text="開始",
            width=120,
            height=50,
            fg_color=self.colors["button"],
            hover_color=self.colors["button_hover"],
            font=("Arial", 18, "bold"),
            command=lambda: self.handle_button_click(
                step_button,
                lambda: self.send_motormanual_operation.send_discrimination_manual_step()
            )
        )
        step_button.pack(pady=10)

        # 中央：原点ボタン
        origin_frame = ctk.CTkFrame(center_panel, fg_color="transparent")
        origin_frame.pack(side='left', expand=True, padx=0)
        
        for i in range(2):
            ctk.CTkLabel(origin_frame, text="判別\nモータ原点復帰" if i == 0 else "返却\nモータ原点復帰", font=("Arial", 16)).pack(pady=5)
            button = ctk.CTkButton(
                origin_frame,
                text="開始" if i == 0 else "開始",
                width=120,
                height=60,
                fg_color=self.colors["button"],
                hover_color=self.colors["button_hover"],
                font=("Arial", 20, "bold"),
                command=lambda x=i: self.handle_button_click(
                    button,
                    lambda: self.send_motor_reset.discrimination_motor_reset() if x == 0 else self.send_motor_reset.return_motor_reset()
                )
            )
            button.pack(pady=(5,5))

        # 右側：数値制御
        control_frame = ctk.CTkFrame(center_panel, fg_color="transparent")
        control_frame.pack(side='right', padx=0)
        
        for i in range(3):
            value_labels = ["投入部\n上昇速度", "判別部\n下降独度", "返却部\n速度変更"]
            value_frame = ctk.CTkFrame(control_frame, fg_color="#404040", corner_radius=10)
            value_frame.pack(side='left', padx=5)
            
            ctk.CTkLabel(value_frame, text=value_labels[i], font=("Arial", 16)).pack(pady=5)
            ctk.CTkButton(
                value_frame,
                text="▲",
                width=60,
                height=30,
                command=lambda x=i: self.adjust_value(x, 1),
                fg_color=self.colors["button"],
                hover_color=self.colors["button_hover"]
            ).pack(pady=2)
            
            value_label = ctk.CTkLabel(
                value_frame,
                text=str(self.values[i]),
                font=("Arial", 24, "bold"),
                width=100,
                height=40
            )
            value_label.pack(pady=2)
            setattr(self, f'value_label_{i}', value_label)
            
            ctk.CTkButton(
                value_frame,
                text="▼",
                width=60,
                height=30,
                command=lambda x=i: self.adjust_value(x, -1),
                fg_color=self.colors["button"],
                hover_color=self.colors["button_hover"]
            ).pack(pady=2)

            button = ctk.CTkButton(
                value_frame,
                text="送信",
                width=70,
                height=40,
                fg_color=self.colors["button"],
                hover_color=self.colors["button_hover"],
                command=lambda x=i: self.handle_button_click(
                    button,
                    lambda: self.send_moter_value1() if x == 0 else self.send_moter_value1() if x == 1 else self.send_moter_value3()
                )
            )
            button.pack(pady=(10, 10))

        # 戻るボタン
        ctk.CTkButton(
            main_frame,
            text="戻る",
            width=300,
            height=55,
            fg_color=self.colors["danger"],
            hover_color="#DC2626",
            font=("Arial", 18, "bold"),
            command=self.timesetting_close
        ).pack(pady=(5,0))

    def adjust_value(self, index, delta):
        self.values[index] = max(1, min(10, self.values[index] + delta))
        getattr(self, f'value_label_{index}').configure(text=str(self.values[index]))

    def timesetting_close(self):
        self.send_potrol_lamp.send_patrol_lamp_stop()
        self.master.destroy()

    def moveview(self):
        maneteview = ctk.CTkToplevel(self.master)
        MaintenanceView(maneteview, self.on_setting_close)

    def sorenoid_view(self):
        sorenoid_view = ctk.CTkToplevel(self.master)
        SorenoidMenteView(sorenoid_view, self.on_setting_close)

    def on_setting_close(self):       
        # self.master.deiconify()
        self.send_potrol_lamp.send_patrol_lamp_stop()
        self.master.destroy()

    def manual_stop(self):
        self.send_motormanual_operation.send_input_manual_stop()

    def send_moter_value1(self):
        value_label1 = self.value_label_0.cget("text")  # 正しい属性名を使用
        value_label2 = self.value_label_1.cget("text")  # 正しい属性名を使用
        self.send_configuration_change.change_input_configuration(int(value_label1),int(value_label2))

    def send_moter_value3(self):
        value_label3 = self.value_label_2.cget("text")  # 正しい属性名を使用
        self.send_configuration_change.change_discrimination_configuration(int(value_label3))

    def show_popup(self):
        """ボタンを押したらポップアップを表示"""

        popup = ctk.CTkToplevel(self.master)  # self.masterを親ウィンドウとして使用
        popup.geometry('400x200')
        popup.overrideredirect(True)
        popup.configure(fg_color='black')
        popup.attributes('-alpha', 1.8)


        # ポップアップを画面中央に配置
        popup.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() - popup.winfo_width()) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - popup.winfo_height()) // 2
        popup.geometry(f"+{x}+{y}")

        label = ctk.CTkLabel(popup, text="送信しました！",font=("Arial", 16), text_color="#FFFFFF")
        label.pack(expand=True)

        # 2秒後にポップアップを自動的に閉じる
        popup.after(2000, lambda: self.close_popup(popup))

    def close_popup(self, popup):
        """ポップアップを閉じて設定画面を最前面に戻す"""
        popup.destroy()  # ポップアップを閉じる
        self.lift()  # 設定画面を最前面に表示

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

    