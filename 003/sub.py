import myapp
from prompt_toolkit.application import get_app_or_none

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import Label
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl

from prompt_toolkit.application import get_app


from io import StringIO
import sys

class Selecter:
	def __init__(self,choices):
		#self.items　--辞書型で名前と実体を管理
		if type(choices) == dict:
			inner = [Row(key) for key in choices.keys()]
			self.items = choices
		else:
			inner = [Row(e) for e in choices]
			self.items = {str(e):e for e in choices}

		#self.label --文字の表示領域
		self.label = Label(text="aaa")
		
		inner = [self.label,]+inner

		layout = HSplit(
			inner,
			key_bindings = defaults_bind(),
		)

		#self.layout --app上の構成
		self.layout = Layout(layout)

		if 0:
			#自身を記録に追加
			myapp.log.append(self)

			#appが起動してなければ、自身のlayoutで起動する
			if get_app_or_none()==None:
				myapp.run(layout=self.layout)

	def run(self):
		myapp.curselecter=self
		myapp.run(layout=self.layout)	


































# 標準出力をリダイレクトするクラス
class StdoutRedirector:
    def __init__(self, output_control):
        self.output_control = output_control
        self._original_stdout = sys.stdout
        self.buffer = StringIO()

    def write(self, text):
        self.buffer.write(text)
        self.output_control.text += text  # フォーカス可能な出力ウィンドウにテキスト追加

    def flush(self):
        self.buffer.flush()

    def __enter__(self):
        sys.stdout = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self._original_stdout

#layoutと選択肢の内容をmyappのlogに保存する
def selecter(choices):
	if type(choices) == dict:
		inner = [Row(key) for key in choices.keys()]
		myapp.log_contents.append(choices)
	else:
		inner = [Row(e) for e in choices]
		myapp.log_contents.append({str(e):e for e in choices})

	label = Label(text="aaa")
	
	myapp.log_label.append(label)

	inner = [label,]+inner

	layout = HSplit(
		inner,
		key_bindings = defaults_bind(),
	)

	layout = Layout(layout)

	myapp.log_layout.append(layout)

	if (app:=get_app_or_none())!=None:
		app.layout = layout
	else:
		myapp.run(layout=layout)

def defaults_bind():

	kb = KeyBindings()

	@kb.add("enter")
	def _(event):
		#選択肢のﾃｷｽﾄを取る
		txt = get_app().layout.current_control.text

		#中身がselecter
		if type((sel:=myapp.curselecter.items[txt])) is Selecter:
			myapp.log.append(myapp.curselecter) #現を保存
			myapp.curselecter = sel
			get_app().layout = sel.layout

		#中身が関数等
		elif callable( (func:=myapp.curselecter.items[txt])):
			with StdoutRedirector(myapp.log[-1].label):
				func()

		#中身がテキスト
		else:
			myapp.curselecter.label.text=txt
		if 0:
			#実行可能なら、実行する
			if callable( (func:=myapp.log[-1].items[txt]) ):
				with StdoutRedirector(myapp.log[-1].label):
					func()
			else:
				myapp.log[-1].label.text = txt 

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
		self.text = str(text) if not callable(text) else "<lambda>"
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

"""
Selecter([
	"aaa",
	"iii",
	"uuu",
])
"""

Selecter({
	"aaa":"aaa",
	"iii":"iii",
	"uuu":"uuu",
	"func":Selecter(["aaa",])
}).run()

