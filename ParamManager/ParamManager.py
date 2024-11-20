import time

class ParamManager:
    def __init__(self):
        self.input_amount = 6  # 初期値を設定
        self.stocker_values = [0, 0.3, 0.6]  # ストッカーの初期値を設定
        self.start_time = time.time()  # 開始時間を記録

    def get_input_amount(self):
        elapsed_time = time.time() - self.start_time  # 経過時間を計算
        self.input_amount = 6 + int(elapsed_time // 5)  # 5秒ごとにカウントアップ
        return self.input_amount 
    def get_stocker_values(self):
        return self.stocker_values 
