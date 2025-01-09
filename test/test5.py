
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings

#keysを入れて、選択keyを返す
#keys・valsを入れて、選択valを返す
def choicer(items,message=""):

	if type(items)==dict:
		choices = Data([key for key in items.keys()])
	else:
		choices = Data(items)

	#prompt_toolkitのパーツをつくる
	innerparts=FormattedTextControl(text=choices.render())

	window = Window(
		content=innerparts,
		always_hide_cursor = True,
	)

	root_container=HSplit([window])
	layout = Layout(container=root_container)

	# アプリケーションの作成
	app = Application(
		layout=layout,
		key_bindings=mybind(choices,innerparts),
		full_screen=True,
	)
	#実行
	app.run()


	if type(items)==dict:
		res = items[choices.res]
	else:
		res=choices.res
	
	return res

#文字列ﾃﾞｰﾀを保存する箱
class Data:
	def __init__(self,names):
		self.names  = names 
		self.base  = "#44ff00"
		self.stl   = "#ff0066"
		self.__index = 0
		self.res=None

	@property
	def index(self):
		return self.__index

	@index.setter
	def index(self,index):
		if len(self.names)<=index:
			self.__index=len(self.names)-1
		elif index<0:
			self.__index=0
		else:
			self.__index=index

	def render(self):
		basestyle=self.base
		style=self.stl
		tmp = [(basestyle,name+"\n") if self.__index!=i else (style,name+"\n") for i,name in enumerate(self.names)]
		return FormattedText(tmp)

def mybind(data,parent):
	# キーバインディングを作成
	bindings = KeyBindings()

	@bindings.add('q')
	def exit_app(event):
		event.app.exit()

	@bindings.add('up')
	def up(event):
		data.index -= 1
		parent.text=data.render()

	@bindings.add('down')
	def dataown(event):
		data.index += 1
		parent.text=data.render()

	@bindings.add('enter')
	def ent(event):
		event.app.exit()
		data.res=data.names[data.index]

	return bindings


x = choicer(["aaa","iii","uuu"])
y = choicer({
"aaa":100,
"iii":200,
"uuu":300,
})

print(x,y)
