from prompt_toolkit.application import get_app
from prompt_toolkit.layout import Window
from prompt_toolkit.layout.controls import FormattedTextControl

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
			self.control,
			height=1,
			style=get_style,
			always_hide_cursor=True,
		)

	def __pt_container__(self) -> Window:
		return self.window
