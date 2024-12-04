import time
from ui.EarPop.EarPopup import ErrorPopup 

class ParamManager:
    def __init__(self, master):
        self.input_amount = 6  # 投入量を設定
        self.stocker_values = [0.1, 0.9, 0.6]  # ストッカーの初期値を設定
        self.start_time = time.time() 
        self.error_popup = ErrorPopup(master) 

    def get_input_amount(self):
        elapsed_time = time.time() - self.start_time 
        self.input_amount = 6 + int(elapsed_time // 5)  
        return self.input_amount 
    
    def get_stocker_values(self):
        return self.stocker_values 

    def show_error(self, error_code):
        """error_codeにエラーコードを入力されると表示される"""
        self.error_popup.show_error(error_code) 
