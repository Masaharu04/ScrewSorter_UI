import subprocess
from datetime import datetime


class RtcControl():
	def __init__(self):
		pass
	def set_system_date(self, input_date):#'2025-01-30 15:30:00'
		# コマンドをリストとして渡す
		command = ['sudo', 'date', '--set=2000-01-01 00:00:00']
		command[2] = '--set=' + input_date
		# subprocess.run()を使ってコマンドを実行
		result = subprocess.run(command, capture_output=True, text=True)

		# コマンドが正常に実行されたかを確認
		if result.returncode == 0:
			print("コマンドは成功しました")
		else:
			print(f"コマンドは失敗しました。エラーコード: {result.returncode}")
			print(f"エラーメッセージ: {result.stderr}")
	def set_rtc_date_used_by_system_date(self):
		# コマンドをリストとして渡す
		command = ['sudo', 'hwclock', '-w']
		# subprocess.run()を使ってコマンドを実行
		result = subprocess.run(command, capture_output=True, text=True)

		# コマンドが正常に実行されたかを確認
		if result.returncode == 0:
			print("コマンドは成功しました")
		else:
			print(f"コマンドは失敗しました。エラーコード: {result.returncode}")
			print(f"エラーメッセージ: {result.stderr}")
	def set_date(self, input_date):
		date_buf = datetime.strptime(input_date, "%Y/%m/%d/%H/%M")
		formatted_date = date_buf.strftime("%Y-%m-%d %H:%M")
		formatted_date = formatted_date + ':00'
		self.set_system_date(formatted_date)
		self.set_rtc_date_used_by_system_date()
		
		
rtc_control = RtcControl()
rtc_control.set_date('2025/01/31/13/30')



