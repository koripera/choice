from prompt_toolkit.application import Application

mainselecter=None
curselecter=None
log = []
log_layout = []
log_contents = []
log_label = []

def run(layout):
	app = Application(
		layout=layout,
		full_screen=True,
	)

	app.run()

	
