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


"""
focus_next()は末端のフォーカスを順繰りに移動
focus(obj)で絶対的に指定したい

func(Selecter())のような使い方をしたい
menuクラスをつくる？
"""

#選択valを返す
def selecter(items):

	return items[0]

#Menuかcallableをvalに持って、選択で実行
class Menu:
	def __init__(
		self,
		items        : list[ tuple[ str,type[Self] | Callable[..., Any] ] ],      
		message      : str = "",
		)           -> None:

		#前のmenuに戻る
		def back():
			myapp.log.pop(-1)
			get_app().layout = myapp.log[-1].layout
			get_app().layout.focus(myapp.log[-1].command)


		#self.items 　--[(name,val)...]の選択するｺﾝﾃﾝﾂ
		#self.rowlist --選択肢の行のwindowﾘｽﾄ	
		self.items   = [("back",back),] + items
		self.message = message    
		self.rowlist = [Row(name) for name,val in self.items]

		#self.label --文字の表示領域
		#情報を表示するlayout
		self.console_area = TextArea(text="aaa")
		self.message_area = Label(text=self.message)
		
		self.info_area = [
			self.console_area,
			HorizontalLine(),
		]
		if self.message!="":
			self.info_area.append(self.message_area)

		self.info = HSplit(self.info_area)

		#選択肢だけのlayout
		self.command = HSplit(self.rowlist)

		#総合のlayout
		layout = HSplit(
			[self.info,self.command],
			key_bindings = DynamicKeyBindings(self.main_kb),
		)

		#self.layout --app上の構成
		self.layout = Layout(layout)

		#主となるコンテンツはtabで切り替えたい
		self.kb = [
			self._info_keys(),
			self._selecter_keys(),
		]
		
		self.mainindex = 1 #
		self.rowindex  = 0 #選択肢の選択行

	#keybind{{{
	def main_kb(self) -> KeyBindings:
		return merge_key_bindings([
			self._common_kb(),
			self.kb[self.mainindex],
		])

	def _common_kb(self) -> KeyBindings:
		kb = KeyBindings()

		@kb.add("tab")
		def _(event):
			self.mainindex+=1
			if self.mainindex >= len(self.kb):
				self.mainindex = 0

			if self.mainindex == 0:
				event.app.layout.focus(self.label)
			elif self.mainindex == 1:
				event.app.layout.focus(self.rowlist[self.rowindex])

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
			#選択肢のﾃｷｽﾄを取る
			txt = get_app().layout.current_control.text

			#中身がMenu
			if type( (select_menu:=self.items[self.rowindex][1] )) is type(self):
				myapp.curselecter = select_menu
				myapp.log.append(myapp.curselecter) #現を保存
				get_app().layout = select_menu.layout
				get_app().layout.focus(select_menu.command)

			#中身が関数等
			elif callable( (select_func:= self.items[self.rowindex][1]) ):
				self.console_area.text=""
				with StdoutRedirector(self.console_area):
					select_func()
	
		return kb
	#}}}

	def run(self):
		#終了用の選択肢を追加する
		def exit():
			get_app().exit()
		self.rowlist[0] = Row("exit")
		self.items[0]   = ("exit", exit)
		self.command.children = [e.__pt_container__() for e in self.rowlist]

		#全体管理
		myapp.mainselecter = self
		myapp.curselecter  = self
		myapp.log.append(myapp.curselecter)

		myapp.run(layout=self.layout,pre_run=self.firstfocus)	
		return 

	def firstfocus(self):
		#self.mainindex = 1
		get_app().layout.focus(self.rowlist[0])

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

