class ParamManager:
    def __init__(self):
        self.input_amount = 2  # 初期値を設定
        self.stocker_values = [0, 0.3, 0.6]  # ストッカーの初期値を設定

    def get_input_amount(self):
        return self.input_amount 
    def get_stocker_values(self):
        return self.stocker_values 
