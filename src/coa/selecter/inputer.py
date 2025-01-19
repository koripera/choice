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
			dont_extend_height=True,
		)
    
		#入力を受け付けるエリア
		self.input_area = TextArea(
			prompt="> ",
			multiline=False,
			focusable=True,
			wrap_lines=False,
			dont_extend_height=True,
		)

		#最終のﾚｲｱｳﾄ		
		self.layout = Layout(
			HSplit([
				output_area, 
				HorizontalLine(),
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



