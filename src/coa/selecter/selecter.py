from typing import Self,Any,Callable
import threading

from prompt_toolkit.application import Application
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

from .row import Row
from .stdoutredirector import StdoutRedirector


#選択valを返す
def selecter(items,message=None):
	event = threading.Event()
	control = _Selecter(items,message,event=event)
	control.run()

	event.wait()
	
	return control.result

class _Selecter:
	def __init__(
		self,
		items,      
		message      : str = None,
		event=None,
		)           -> None:

		self.event          = event   #別ｽﾚｯﾄﾞで実行する用の停止ｲﾍﾞﾝﾄ
		self.result         = None    #最終返す値

		self.base_items     = items   #基本となるｺﾏﾝﾄﾞ名とｺﾏﾝﾄﾞ
		self.display_items  = items   #表示用のｺﾏﾝﾄﾞ名とｺﾏﾝﾄﾞ
		self.message        = message #ｺﾏﾝﾄﾞ前に表示されるstrまたは表示を行う関数
		self.previous       = None    #直前のｲﾝｽﾀﾝｽ
		self._layout        = None    #基本となるLayout

		self._make_layout()           #基本layout作成

	def message_reset(self):
		if type(self.message) == str:
			self.message_area.text = self.message
		elif self.message != None:
			stdout = StdoutRedirector()
			with stdout:
				tail = self.message()

			if type(tail)==str:
				stdout.capture += tail

			self.message_area.text = stdout.capture

	@property
	def layout(self):
		return self._layout

	def _make_layout(self):
		#self.rowlist --選択肢の行のwindowﾘｽﾄ	
		self.rowlist = [Row(name) for name,val in self.display_items]

		#情報を表示するlayout
		self.message_area = Label(text="")
		
		#選択肢だけのlayout
		self.command = HSplit(self.rowlist)

		#messageの有無でlayout変更
		if self.message==None  : inner=[self.command]
		else                   : inner=[self.message_area,HorizontalLine(),self.command]

		#総合のlayout
		layout = HSplit(
			[ScrollablePane(HSplit(inner))],
			key_bindings = DynamicKeyBindings(self.main_kb),
		)

		#self.layout --app上の構成
		self._layout = Layout(layout)
		
		self.message_reset()

		self.rowindex  = 0 #選択肢の選択行


	def run(self):
		#ｱﾌﾟﾘの起動状態を取る
		if (app:=get_app_or_none()) != None:
			#layoutを保存して置き換え
			self.previous = app.layout
			app.layout    = self.layout
		else:
			app = Application(
				layout=self.layout,
				full_screen=True,
			)
			app.run()
		app.layout.focus(self.command)
			

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
			self.result = self.display_items[self.rowindex][1]
			self.event.set()
			
			if self.previous == None:
				event.app.exit()
			else:
				event.app.layout = self.previous
					


		return kb
	#}}}keybind

