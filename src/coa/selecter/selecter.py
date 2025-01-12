from io import StringIO
import sys
from typing import Self,Any,Callable

from prompt_toolkit.application import (
	get_app,
	get_app_or_none,
)
from prompt_toolkit.layout import (
	Layout,
	HSplit,
	Window,
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

#選択valを返す
def selecter(items,message=""):
	event = threading.Event()
	control = _Selecter(items,message,event=event)
	control.run()

	event.wait()
	
	return control.result

class _Selecter:
	def __init__(
		self,
		items        : list[ tuple[ str,type[Self] | Callable[..., Any] ] ],      
		message      : str = "",
		event=None,
		)           -> None:

		self.event = event

		#self.items 　--[(name,val)...]の選択するｺﾝﾃﾝﾂ
		#self.rowlist --選択肢の行のwindowﾘｽﾄ	
		self.items   = items
		self.message = message    
		self.rowlist = [Row(name) for name,val in self.items]

		#情報を表示するlayout
		self.message_area = Label(text=self.message)
		
		#選択肢だけのlayout
		self.command = HSplit(self.rowlist)

		if self.message=="":inner=[self.command]
		else               :inner=[self.message_area,self.command]

		#総合のlayout
		layout = HSplit(
			inner,
			key_bindings = DynamicKeyBindings(self.main_kb),
		)

		#self.layout --app上の構成
		self.layout = Layout(layout)
		
		self.rowindex  = 0 #選択肢の選択行

		self.oldlayout = None #直前のlayout(単独で開いているか)
		self.result = None

	def run(self):
		#ｱﾌﾟﾘの起動状態を取る
		if (app:=get_app_or_none()) != None:
			#layoutを保存して置き換え
			self.oldlayout = app.layout
			app.layout = self.layout
		else:
			myapp.run(layout=self.layout)
			

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

		@kb.add("down")
		@kb.add("j")
		def _(event):
			self.rowindex+=1
			if self.rowindex >= len(self.rowlist):
				self.rowindex=0
			event.app.layout.focus(
				self.rowlist[self.rowindex]
			)

		@kb.add("up")
		@kb.add("k")
		def _(event):
			self.rowindex-=1
			if self.rowindex < 0:
				self.rowindex = len(self.rowlist)-1
			event.app.layout.focus(
				self.rowlist[self.rowindex]
			)

		@kb.add("enter")
		def _(event):
			self.result = self.items[self.rowindex][1]
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

