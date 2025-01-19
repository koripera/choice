from io import StringIO
import sys

from prompt_toolkit.eventloop import call_soon_threadsafe

# 標準出力を変数に格納する
class StdoutRedirector:
	def __init__(self, output_control=None):
		self.output_control = output_control
		self._original_stdout = sys.stdout
		self.buffer = StringIO()
		self.capture = "" #変数として保存

	def write(self, text):
		#self.buffer.write(text)
		self.capture += text   #str変数に
		#if self.output_control:
			# スレッドセーフにUIを更新
		#	call_soon_threadsafe(lambda: self.update_output(text))

	def update_output(self, text):
		# フォーカス可能な出力ウィンドウにテキスト追加
		self.output_control.text += text
		get_app().invalidate() #即時更新したいが、意味なさそう

	def flush(self):
		self.buffer.flush()

	def __enter__(self):
		sys.stdout = self
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		sys.stdout = self._original_stdout

