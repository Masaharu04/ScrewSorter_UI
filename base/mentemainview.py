import customtkinter as ctk
from base.menteviews import MaintenanceView
class MaintenanceMainView:
    def __init__(self, master, on_close, motervalue):
        self.master = master
        self.on_close = on_close
        self.motervalue = motervalue
        
        # カスタムカラーの定義
        self.colors = {
            "background": "#1E1E1E",    # ダークモード背景
            "button": "#3B82F6",        # モダンなブルー
            "button_hover": "#2563EB",   # ホバー時の濃いブルー
            "danger": "#EF4444",        # 警告用レッド
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
        left_button_frame.pack(side='left', padx=0)
        
        ctk.CTkButton(
            left_button_frame,
            text="←",
            width=60,
            height=260,
            fg_color=self.colors["button"],
            hover_color=self.colors["button_hover"],
            font=("Arial", 18, "bold"),
            command=self.moveview
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
            font=("Arial", 18, "bold")
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
            
            ctk.CTkLabel(control_frame, text=f"制御 {i+1}", font=("Arial", 16)).pack()
            
            button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
            button_frame.pack(pady=5)
            
            ctk.CTkButton(
                button_frame,
                text="ON",
                width=90,
                height=50,
                fg_color=self.colors["button"],
                hover_color=self.colors["button_hover"],
                font=("Arial", 16, "bold")
            ).pack(side='left', padx=5)
            
            ctk.CTkButton(
                button_frame,
                text="OFF",
                width=90,
                height=50,
                fg_color=self.colors["danger"],
                hover_color="#DC2626",
                font=("Arial", 16, "bold")
            ).pack(side='left', padx=5)

        # 中央パネル
        center_panel = ctk.CTkFrame(container, fg_color=self.colors["panel"], corner_radius=15)
        center_panel.pack(side='left', expand=True, fill='both', pady=0, padx=0)  # 左に寄せるためにside='left'を追加

        # 左側：STEPボタン
        step_frame = ctk.CTkFrame(center_panel, fg_color="transparent")
        step_frame.pack(side='left', padx=20)
        
        ctk.CTkLabel(step_frame, text="STEPボタン", font=("Arial", 16)).pack(pady=5)
        ctk.CTkButton(
            step_frame,
            text="STEP",
            width=120,
            height=50,
            fg_color=self.colors["button"],
            hover_color=self.colors["button_hover"],
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # 中央：原点ボタン
        origin_frame = ctk.CTkFrame(center_panel, fg_color="transparent")
        origin_frame.pack(side='left', expand=True, padx=0)
        
        for i in range(2):
            ctk.CTkLabel(origin_frame, text=f"原点{i+1}", font=("Arial", 16)).pack(pady=5)
            ctk.CTkButton(
                origin_frame,
                text="原点",
                width=120,
                height=60,
                fg_color=self.colors["button"],
                hover_color=self.colors["button_hover"],
                font=("Arial", 20, "bold")
            ).pack(pady=0)

        # 右側：数値制御
        control_frame = ctk.CTkFrame(center_panel, fg_color="transparent")
        control_frame.pack(side='right', padx=0)
        
        for i in range(3):
            value_frame = ctk.CTkFrame(control_frame, fg_color="#404040", corner_radius=10)
            value_frame.pack(side='left', padx=5)
            
            ctk.CTkLabel(value_frame, text=f"値{i+1}", font=("Arial", 16)).pack(pady=5)
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

        # 戻るボタン
        ctk.CTkButton(
            main_frame,
            text="戻る",
            width=200,
            height=45,
            fg_color=self.colors["danger"],
            hover_color="#DC2626",
            font=("Arial", 18, "bold"),
            command=self.timesetting_close
        ).pack(side='bottom', pady=10)

    def adjust_value(self, index, delta):
        self.values[index] = max(1, min(10, self.values[index] + delta))
        getattr(self, f'value_label_{index}').configure(text=str(self.values[index]))

    def timesetting_close(self):
        self.master.destroy()

    def moveview(self):
        maneteview = ctk.CTkToplevel(self.master)
        MaintenanceView(maneteview, self.on_setting_close)

    def on_setting_close(self):       
        # self.master.deiconify()
        self.master.pack()