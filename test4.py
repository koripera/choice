from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings

"""
選択肢・valを入れて
選択内容を返す
"""


#文字列ﾃﾞｰﾀを保存する箱
class data:
	def __init__(self,names):
		self.names  = names 
		self.base  = "#44ff00"
		self.stl   = "#ff0066"
		self.index = 0
		self.res=None

	def render(self):
		basestyle=self.base
		style=self.stl
		tmp = [(basestyle,name+"\n") if self.index!=i else (style,name+"\n") for i,name in enumerate(self.names)]
		return FormattedText(tmp)

d = data(["aaa","bbb","ccc"])

if 1:
	aaa=FormattedTextControl(text=d.render())

	# FormattedTextControl を使ってテキストを表示
	window = Window(
		content=aaa,
		always_hide_cursor = True,
	)

	# キーバインディングを作成
	bindings = KeyBindings()

	@bindings.add('q')
	def exit_app(event):
		event.app.exit()

	@bindings.add('up')
	def up(event):
		d.index -= 1
		aaa.text=d.render()

	@bindings.add('down')
	def down(event):
		d.index += 1
		aaa.text=d.render()

	@bindings.add('enter')
	def ent(event):
		event.app.exit()
		d.res=d.names[d.index]
		







	# レイアウトに追加
	root_container = HSplit([window])
	layout = Layout(container=root_container)

	# アプリケーションの作成
	app = Application(
		layout=layout,
		key_bindings=bindings,
		full_screen=True,
	)

	# アプリケーションの実行
	app.run()

	print(d.res)


