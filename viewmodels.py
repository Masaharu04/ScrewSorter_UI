class MainViewModel:
    def __init__(self):
        self.output_text = ""

    def update_output_text(self, message):
        """出力メッセージを更新"""
        self.output_text = message
        return self.output_text

    def show_warning(self):
        """警告メッセージを表示"""
        return "設定を変更しようとしています。よろしいですか？"
