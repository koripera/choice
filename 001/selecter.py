from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings

from prompt_toolkit.application import get_app
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.application import get_app

"""
まとめたlayoutを返す

choice
ﾘｽﾄ･ﾀﾌﾟﾙ、その要素のstrで表示、要素を返す
辞書、そのkeyで表示、valを返す
"""

class common():
	pass

def selecter(choices):

	if type(choices) == dict:
		inner = [Row(key) for key in choices.keys()]
	else:
		inner = [Row(e) for e in choices]

	layout = HSplit(
		inner,
		key_bindings = defaults_bind(),
		#style        = defaults_style(),
	)

	layout = Layout(layout)

	return layout



def defaults_bind():

	kb = KeyBindings()

	def aa_(event,dataclass):
		cur = event.app.layout.current_control
		dataclass.text=cur.text
		event.app.exit()

	qqq = lambda event :aa_(event,dataclass=common) 
	#kb.add("enter")(qqq)
	
	@kb.add("enter")
	def _(event):
		print(get_app().layout.current_control)
		print(get_app().layout.current_window)
		print(get_app().layout.current_buffer)
		print(get_app().layout.container.children)
	
	@kb.add("j")
	def _(event):
		#print(event.app.layout.focused_element)
		get_app().layout.focus_next()

	@kb.add("k")
	def _(event):
		get_app().layout.focus_previous()

	@kb.add("q", eager=True)
	def _(event):
		event.app.exit()

	return kb

def defaults_style():
	style = Style.from_dict({
		"row"         : "",
		"row.focused" : "reverse",
	})

	return style

class Row:
#最終は__pt_container__で返すものでappに登録される。
	def __init__(self,text: str,) -> None:
		self.text = text
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

