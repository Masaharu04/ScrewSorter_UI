import csv
from pathlib import Path
from datetime import datetime
import shutil
from datetime import timedelta
from pathlib import Path

class CsvControl:
    def __init__(self, current_time, dir_path, usb_dir_path
                 , discrimination_results_file_path, every_five_minute_file_path, daily_file_path
                 , discrimination_results_header, every_five_minute_file_header, daily_file_header):
        self.output_flag = 0
        self.daily_file_length = 0
        self.dir_path = dir_path
        self.usb_dir_path = usb_dir_path
        self.discrimination_results_file_path = discrimination_results_file_path
        self.every_five_minute_file_path = every_five_minute_file_path
        self.daily_file_path = daily_file_path
        self.discrimination_results_header = discrimination_results_header
        self.every_five_minute_file_header = every_five_minute_file_header
        self.daily_file_header = daily_file_header
        self.time_buf = self.edit_time(current_time, -(self.get_minute(current_time)%5))
        self.create_new_file(self.discrimination_results_file_path,self.discrimination_results_header)
        self.create_new_file(self.every_five_minute_file_path,self.every_five_minute_file_header)
        self.create_new_file(self.daily_file_path,self.daily_file_header)
        list_data = self.read_csv_file(self.discrimination_results_file_path)
        if(len(list_data) >= 1):
            if self.get_elapsed_time(list_data[0][0], self.time_buf) >=5:
                discrimination_results = self.tally_discrimination_results(self.edit_time(list_data[-1][0], (5-self.get_minute(list_data[-1][0])%5)), list_data)
                self.add_a_line_of_csv_data(self.every_five_minute_file_path, discrimination_results)
                self.clean_csv_file(self.discrimination_results_file_path, self.discrimination_results_header)
        list_data = self.read_csv_file(self.every_five_minute_file_path)
        if(len(list_data) >= 1):
            if (self.get_elapsed_time(list_data[0][0], self.time_buf) > 0 and self.get_day(list_data[0][0]) != self.get_day(self.time_buf)):
                daily_result = self.tally_results_every_five_minutes(list_data[0][0], list_data)
                self.add_a_line_of_csv_data(self.daily_file_path, daily_result)
                self.clean_csv_file(self.every_five_minute_file_path, self.every_five_minute_file_header)
        list_data = self.read_csv_file(self.daily_file_path)
        self.daily_file_length = len(list_data)
        if self.daily_file_length > 30:
            list_data = list_data[-30:]
            self.clean_csv_file(self.daily_file_path, self.daily_file_header)
            self.add_some_csv_data(self.daily_file_path, list_data)
            self.daily_file_length = 30
    def add_a_line_of_csv_data(self, file_path, csv_data):
        with open(file_path, 'a', encoding='utf-8', newline='') as f:
            dataWriter = csv.writer(f)
            dataWriter.writerow(csv_data)
    def add_some_csv_data(self, file_path, csv_data):
        with open(file_path, 'a', encoding='utf-8', newline='') as f:
            dataWriter = csv.writer(f)
            dataWriter.writerows(csv_data)
    def create_new_file(self, file_path, header):
        file_path_obj = Path(file_path)
        # ファイルが存在しなかったら作成する
        if not file_path_obj.exists():
            file_path_obj.touch()
            self.add_a_line_of_csv_data(file_path, header)
    def clean_csv_file(self, file_path, header):
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            self.add_a_line_of_csv_data(file_path, header)
    def get_elapsed_time(self, target_time, current_time) -> int:
        # 入力された日時文字列を分割して年、月、日、時、分を取り出す
        year, month, day, hour, minute = map(int, target_time.split('/'))
        # datetimeオブジェクトを作成
        target_time_obj = datetime(year, month, day, hour, minute)
        # 入力された日時文字列を分割して年、月、日、時、分を取り出す
        year, month, day, hour, minute = map(int, current_time.split('/'))
        # datetimeオブジェクトを作成
        current_time_obj = datetime(year, month, day, hour, minute)
        # 経過時間を計算（秒単位）
        elapsed_time = current_time_obj - target_time_obj
        # 経過時間を分単位で取得
        elapsed_minutes = int(elapsed_time.total_seconds() // 60)
        return elapsed_minutes
    def read_csv_file(self, file_path):
        # sample.csv を読み込む
        with open(file_path) as f:
            reader = csv.reader(f)
            # ヘッダー行をスキップ
            next(reader)
            # CSVファイルの内容をリストに格納
            list_data = [row for row in reader]
            return list_data
    def tally_discrimination_results(self, current_time, list_data) -> list:
        result_data = [current_time, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for row in list_data:
            if row[1] == '-1':
                result_data[10] += 1
            elif row[1] == '0':
                result_data[9] += 1
            elif row[1] == '5':
                if row[2] == '8':
                    result_data[1] += 1
                elif row[2] == '10':
                    result_data[2] += 1
                elif row[2] == '12':
                    result_data[3] += 1
                elif row[2] == '16':
                    result_data[4] += 1
            elif row[1] == '6':
                if row[2] == '8':
                    result_data[5] += 1
                elif row[2] == '10':
                    result_data[6] += 1
                elif row[2] == '12':
                    result_data[7] += 1
                elif row[2] == '16':
                    result_data[8] += 1
        return result_data
    def tally_results_every_five_minutes(self, current_time, list_data) -> list:
        # スラッシュで分割し、最初の3つの要素を取り出して再結合
        time_buf = '/'.join(current_time.split('/')[:3])
        result_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for row in list_data:
            row[0] = 0
            # 要素ごとに足し合わせる
            result_data = [int(a) + b for a, b in zip(row, result_data)]
        result_data[0] = time_buf
        return result_data
    def get_minute(self, current_time) -> int:
        # スラッシュで分割し、最後の要素を取得
        minute_num = current_time.split('/')[-1]
        return int(minute_num)
    def get_day(self, current_time) -> int:
        # スラッシュで分割し、最後の要素を取得
        day_num = current_time.split('/')[2]
        return int(day_num)
    def csv_controller(self, current_time):
        if self.get_elapsed_time(self.time_buf, current_time) >= 5:
            list_data = self.read_csv_file(self.discrimination_results_file_path)
            discrimination_results = self.tally_discrimination_results(current_time, list_data)
            self.add_a_line_of_csv_data(self.every_five_minute_file_path, discrimination_results)
            self.clean_csv_file(self.discrimination_results_file_path, self.discrimination_results_header)
            if (self.get_day(self.time_buf) != self.get_day(current_time)):
                list_data = self.read_csv_file(self.every_five_minute_file_path)
                daily_result = self.tally_results_every_five_minutes(self.edit_time(current_time, -1440), list_data)
                self.add_a_line_of_csv_data(self.daily_file_path, daily_result)
                self.clean_csv_file(self.every_five_minute_file_path, self.every_five_minute_file_header)
                if self.daily_file_length >= 30:
                    list_data = self.read_csv_file(self.daily_file_path)
                    list_data = list_data[-30:]
                    self.clean_csv_file(self.daily_file_path, self.daily_file_header)
                    self.add_some_csv_data(self.daily_file_path, list_data)
                else:
                    self.daily_file_length += 1
            self.time_buf = self.edit_time(current_time, -(self.get_minute(current_time)%5))
        self.output_csv()
            
    def edit_time(self, target_time, minute_delta) -> str:
        # 文字列から日付部分（年、月、日）を取得
        year, month, day, hour, minute = map(int, target_time.split('/'))
        # datetimeオブジェクトを作成
        initial_date = datetime(year, month, day, hour, minute)

        # 1日を追加する
        new_date = initial_date + timedelta(minutes = minute_delta)
        # 新しい日付を指定の形式で出力
        formatted_date = new_date.strftime("%Y/%m/%d/%H/%M")
        return formatted_date
    def request_output_csv(self):
        if self.output_flag == 0:
            self.output_flag = 1
    def output_csv(self):
        if self.output_flag > 0:
            if Path(self.usb_dir_path).is_dir():
                try:
                    # ディレクトリをコピー
                    shutil.copytree(self.dir_path, self.usb_dir_path, dirs_exist_ok=True)
                    #print(f"ディレクトリをコピーしました: {self.dir_path} -> {self.usb_dir_path}")
                except Exception as e:
                    print(f"エラーが発生しました: {e}")
                finally:
                    self.output_flag = 0
            else:
                print("ディレクトリが存在しません")
                self.output_flag = 0

    #########################test_code#########################
    def date_add(self, time_num) -> str:
        # 文字列から日付部分（年、月、日）を取得
        year, month, day, hour, minute = map(int, time_num.split('/'))
        # datetimeオブジェクトを作成
        initial_date = datetime(year, month, day, hour, minute)

        # 1日を追加する
        new_date = initial_date + timedelta(minutes=1)
        # 新しい日付を指定の形式で出力
        formatted_date = new_date.strftime("%Y/%m/%d/%H/%M")
        return formatted_date