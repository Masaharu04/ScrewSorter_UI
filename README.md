# ScrewSorter_UI

## ディレクトリ構成
```
components/
├── src/
│   ├── pycache/
│   ├── base/
│   │   ├── menteviews.py
│   │   ├── settingviews.py
│   │   └── views.py
│   └── img/
├── ui/
│   ├── EarPop/
│   │   ├── _pycache_/
│   │   └── EarPopup.py
│   ├── export/
│   │   ├── _pycache_/
│   │   └── export.py
│   ├── InputAmount/
│   │   └── InputAmount.py
│   ├── Shutdown/
│   │   └── Shutdown.py
│   └── UnderButton/
│       ├── _pycache_/
│       └── UnderButton.py
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
Windowas
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


