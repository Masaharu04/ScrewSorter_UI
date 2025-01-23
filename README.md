# ScrewSorter_UI

## ディレクトリ構成
```
components/
├── src/
│   ├── ParamManager/
│   │   └── ParamManager.py 
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

## 初期インストール方法
1. リポジトリをクローン
```bash
git clone [リポジトリのURL]
cd [プロジェクトディレクトリ]
```
2. 仮想環境の構築
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

4. パッケージのインストール
```
pip install customtkinter Pillow
```
```
pip install pyserial
```

## 実行方法
ターミナルで以下のコマンドを実行してください：
```bash
source myenv/bin/activate
```
```
python3 main.py
```


