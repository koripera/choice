from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app

mainselecter=None
curselecter=None
log = []
log_layout = []
log_contents = []
log_label = []

def run(layout):
	app = Application(
		layout=layout,
		full_screen = True,
	)

	app.run()

def initial_focus(app):
	app.layout.focus_next()
	
	
