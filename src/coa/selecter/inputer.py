from io import StringIO
import sys
from typing import Self,Any,Callable

from prompt_toolkit import prompt

from prompt_toolkit.application import (
	get_app,
	get_app_or_none,
)
from prompt_toolkit.layout import (
	Layout,
	HSplit,
	Window,
	ScrollablePane,
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import (
	KeyBindings,
	merge_key_bindings,
	DynamicKeyBindings,
)
from prompt_toolkit.widgets import (
	Label,
	HorizontalLine,
	TextArea,
)

from . import myapp

import threading

#入力valを返す
def inputer(message=""):
	event = threading.Event()
	control = _Inputer(message,event=event)
	control.run()

	event.wait()

	#res = prompt(message)#これもイベントループの一種？

	return control.result

class _Inputer:
	def __init__(
		self,
		message      : str = "",
		event=None,
		)           -> None:

		self.event = event
		self.message = message

		#message表示エリア
		output_area = TextArea(
			text=self.message,
			multiline=True,
			focusable=False,
			wrap_lines=True,
			read_only=True,
			height=2,
		)
    
		#入力を受け付けるエリア
		self.input_area = TextArea(
			height=3,
			prompt="> ",
			multiline=False,
			focusable=True,
			wrap_lines=False
		)

		#最終のﾚｲｱｳﾄ		
		self.layout = Layout(
			HSplit([
				output_area, 
				Window(height=1, char="-"),
				self.input_area,
			],
			key_bindings = DynamicKeyBindings(self.main_kb),
			)
		)

		self.oldlayout = None #直前のlayout(単独で開いているか)
		self.result = None

	def run(self):
		#ｱﾌﾟﾘの起動状態を取る

		#起動されてるなら、layout置き換え
		if (app:=get_app_or_none()) != None:
			self.oldlayout = app.layout
			app.layout = self.layout
		#されてないなら、新規に起動
		else:
			myapp.run(layout=self.layout)
		app.layout.focus(self.input_area)
			

	#keybind{{{
	def main_kb(self) -> KeyBindings:
		return merge_key_bindings([
			self._common_kb(),
			self._selecter_keys(),
		])

	def _common_kb(self) -> KeyBindings:
		kb = KeyBindings()

		@kb.add("escape", eager=True)
		def _(event):
			event.app.exit()

		return kb

	def _info_keys(self) -> KeyBindings:
		kb = KeyBindings()
		
		return kb

	def _selecter_keys(self) -> KeyBindings:
		kb = KeyBindings()

		@kb.add("enter")
		def _(event):
			user_input = self.input_area.text.strip()
			#入力が行われた
			if user_input:
				self.result = user_input
				self.event.set()
			
				if self.oldlayout == None:
					event.app.exit()

				else:
					event.app.layout = self.oldlayout			


		return kb
	#}}}keybind




# 標準出力をリダイレクトするクラス
class StdoutRedirector:
    def __init__(self, output_control):
        self.output_control = output_control
        self._original_stdout = sys.stdout
        self.buffer = StringIO()

    def write(self, text):
        self.buffer.write(text)
        self.output_control.text += text  # フォーカス可能な出力ウィンドウにテキスト追加

    def flush(self):
        self.buffer.flush()

    def __enter__(self):
        sys.stdout = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self._original_stdout

class Row:
#最終は__pt_container__で返すものでappに登録される。
	def __init__(self,text: str,) -> None:
		self.text = str(text) if not callable(text) else text.__name__
		self.control = FormattedTextControl(
			self.text,
			focusable=True,
		)

		def get_style() -> str:
			if get_app().layout.has_focus(self):
				return "reverse"
			else:
				return ""

		self.window = Window(
			self.control, height=1, style=get_style, always_hide_cursor=True
		)

	def __pt_container__(self) -> Window:
		return self.window

