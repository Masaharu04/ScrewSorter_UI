import sys
import os

# プロジェクトのルートディレクトリをパスに追加
current_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(current_dir)

from src.base.views import start_main_view

if __name__ == "__main__":
    start_main_view()