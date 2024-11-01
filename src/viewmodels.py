class MainViewModel:
    def __init__(self):
        self.output_text = ""
        self.current_error_code = None

    def update_output_text(self, message):
        """出力メッセージを更新"""
        self.output_text = message
        return self.output_text

    def show_warning(self):
        """警告メッセージを表示"""
        self.viewmodel.set_error_code("E001")

        return "設定を変更しようとしています。よろしいですか？"

    def get_error_code(self):
        """現在のエラーコードを取得"""
        return self.current_error_code

    def set_error_code(self, error_code):
        """エラーコードを設定"""
        self.current_error_code = error_code
