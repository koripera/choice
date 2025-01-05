from prompt_toolkit.application import Application

from selecter import selecter

def onechoice():
	app = Application(
		full_screen=True,
		layout = selecter(["aaa","iii","uuu"])
	)
	app.run()

print(onechoice())
