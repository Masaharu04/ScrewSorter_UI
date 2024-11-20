# ScrewSorter_UI

## ディレクトリ構成
```
components/
├── src/
│   ├── base/
│   │   ├── menteviews.py メンテナンス画面
│   │   ├── settingviews.py　設定画面
│   │   └── views.py　メイン画面
│   └── img/　ボタンアイコン画像フォルダー
├── ui/
│   ├── EarPop/
│   │   └── EarPopup.py　エラーポップの処理
│   ├── export/
│   │   └── export.py　出力ボタンの処理
│   ├── InputAmount/
│   │   └── InputAmount.py　投入量の処理
│   ├── Shutdown/
│   │   └── Shutdown.py　シャットダウンボタンを押した際の処理
│   └── UnderButton/
│       └── UnderButton.py　メイン画面の下部の処理
├── main.py　
├── viewmodels.py
└── test.py
```

## 必要環境
- Python 3.12.6

## インストール方法
1. リポジトリをクローン
```bash
git clone [リポジトリのURL]
cd [プロジェクトディレクトリ]
```

2. 依存パッケージのインストール（必要な場合）
```bash
pip install customtkinter
pip install Pillow
```

3. 仮想環境の構築（必要な場合）
```bash
python -m venv myenv
```
Linux
```
source myenv/bin/activate
```
Windows
```
myenv\Scripts\activate
```
パッケージのインストール
```
pip install customtkinter Pillow
```

## 実行方法
ターミナルで以下のコマンドを実行してください：
```bash
python3 main.py
```


