from prompt_toolkit.application import Application

log = []


def run(layout):
	app = Application(
		layout=layout,
		full_screen=True,
	)

	app.run()

	
