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

class Row:
	"""Define row.

	Args:
		text: text to print
	"""

	def __init__(
		self,
		text: str,
	) -> None:
		"""Initialize the widget."""
		self.text = text
		self.control = FormattedTextControl(
			self.text,
			focusable=True,
		)

		def get_style() -> str:
			if get_app().layout.has_focus(self):
				return "class:row.focused"
			else:
				return "class:row"

		self.window = Window(
			self.control, height=1, style=get_style, always_hide_cursor=True
		)

	def __pt_container__(self) -> Window:
		"""Return the window object.

		Mandatory to be considered a widget.
		"""
		return self.window

class item:
	pass

layout = HSplit(
	[
		Row("Test1"),
		Row("Test2"),
		Row("Test3"),
	]
)

# Key bindings

kb = KeyBindings()

layout = Layout(layout)

def aa_(event,dataclass):
	cur = event.app.layout.current_control
	dataclass.text=cur.text
	event.app.exit()

qqq = lambda event :aa_(event,dataclass=item) 
kb.add("enter")(qqq)
	

@kb.add("j")
def _(event):
	layout.focus_next()

@kb.add("k")
def _(event):
	layout.focus_previous()

#@kb.add("enter")
#def _(event):
#	cur = event.app.layout.current_control
#	outside=cur.text
#	event.app.exit()

@kb.add("q", eager=True)
def _(event):
	event.app.exit()

# Styles

style = Style(
	[
		("row", "bg:#073642 #657b83"),
		("row.focused", "bg:#002b36 #657b83"),
	]
)

style = Style.from_dict({
	"row"         : "",
	"row.focused" : "reverse",
})

# Application

app = Application(
	layout=layout,
	full_screen=False,
	key_bindings=kb,
	style=style,
)

app.run()
print(item.text)
