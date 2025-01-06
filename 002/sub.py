import myapp
from prompt_toolkit.application import get_app_or_none

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import Label
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl

from prompt_toolkit.application import get_app

def selecter(choices):
	if type(choices) == dict:
		inner = [Row(key) for key in choices.keys()]
	else:
		inner = [Row(e) for e in choices]

	inner = [Label(text="aaa"),]+inner

	layout = HSplit(
		inner,
		key_bindings = defaults_bind(),
	)

	layout = Layout(layout)

	if (app:=get_app_or_none())!=None:
		app.layout = layout
	else:
		myapp.run(layout=layout)

def defaults_bind():

	kb = KeyBindings()

	@kb.add("j")
	def _(event):
		get_app().layout.focus_next()

	@kb.add("k")
	def _(event):
		get_app().layout.focus_previous()

	@kb.add("q", eager=True)
	def _(event):
		event.app.exit()

	return kb

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

selecter(["aaa","bbb","ccc"])

