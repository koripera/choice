import myapp
from prompt_toolkit.application import get_app_or_none

from prompt_toolkit.key_binding import KeyBindings,merge_key_bindings,DynamicKeyBindings
from prompt_toolkit.widgets import Label,HorizontalLine,TextArea
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl

from prompt_toolkit.application import get_app


from io import StringIO
import sys

"""
focus_next()は末端のフォーカスを順繰りに移動
focus(obj)で絶対的に指定したい
"""

class Selecter:
	def __init__(self,choices):
		#self.rowlist --選択肢の行のwindowﾘｽﾄ
		#self.items　--辞書型で名前と実体を管理
		if type(choices) == dict:
			self.rowlist = [Row(key) for key in choices.keys()]
			self.items = choices
		else:
			self.rowlist = [Row(e) for e in choices]
			self.items = {str(e):e for e in choices}

		#self.label --文字の表示領域
		#情報を表示するlayout
		self.label = TextArea(text="aaa") #Label(text="aaa")
		self.info = HSplit(
			[self.label,HorizontalLine()],
		)

		#選択肢だけのlayout
		self.sel = HSplit(
			self.rowlist,
		)


		#総合のlayout
		layout = HSplit(
			[self.info,self.sel],
			key_bindings = DynamicKeyBindings(self.main_kb),
		)

		#self.layout --app上の構成
		self.layout = Layout(layout)

		#主となるコンテンツはtabで切り替えたい
		self.kb = [
			(self.info , self._info_keys()    ),
			(self.sel  , self._selecter_keys() ),
		]
		
		self.mainindex = 0 #
		self.rowindex  = 0 #選択肢の選択行

	def main_kb(self):
		return merge_key_bindings([
			self._common_kb(),
			self.kb[self.mainindex][1],
		])

	def _common_kb(self):
		kb = KeyBindings()

		@kb.add("tab")
		def _(event):
			self.mainindex+=1
			if self.mainindex >= len(self.kb):
				self.mainindex = 0

			if self.mainindex == 0:
				event.app.layout.focus(self.label)
			elif self.mainindex == 1:
				event.app.layout.focus(self.rowlist[self.rowindex])

		@kb.add("q")
		def _(event):
			event.app.exit()

		return kb

	def _info_keys(self):
		kb = KeyBindings()

		

		return kb

	def _selecter_keys(self):
		kb = KeyBindings()

		@kb.add("j")
		def _(event):
			self.rowindex+=1
			if self.rowindex >= len(self.rowlist):
				self.rowindex=0
			event.app.layout.focus(
				self.rowlist[self.rowindex]
			)

		@kb.add("k")
		def _(event):
			self.rowindex-=1
			if self.rowindex < 0:
				self.rowindex = len(self.rowlist)-1
			event.app.layout.focus(
				self.rowlist[self.rowindex]
			)

		@kb.add("enter")
		def _(event):
			#選択肢のﾃｷｽﾄを取る
			txt = get_app().layout.current_control.text

			#中身がselecter
			if type((sel:=myapp.curselecter.items[txt])) is Selecter:
				myapp.log.append(myapp.curselecter) #現を保存
				myapp.curselecter = sel
				get_app().layout = sel.layout
				get_app().layout.focus(sel.sel)

			#中身が関数等
			elif callable( (func:=myapp.curselecter.items[txt])):
				with StdoutRedirector(myapp.log[-1].label):
					func()

			#中身がテキスト
			else:
				myapp.curselecter.label.text=txt		
		return kb

	def run(self):
		myapp.curselecter=self
		myapp.run(layout=self.layout)	
		return 


class ringlist:
	def __init__(self,l):
		self.index = 0
		self.max   = len(l)
		self.list  = l

	def next(self):
		pass

	def back(self):
		pass






























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


def window_bind():
	kb = KeyBindings()

	@kb.add("tab")
	def _(event):
		pass

	return kb

def defaults_bind():

	kb = KeyBindings()

	@kb.add("tab")
	def _(event):
		get_app().layout.container.focus_next()

	@kb.add("enter")
	def _(event):
		#選択肢のﾃｷｽﾄを取る
		txt = get_app().layout.current_control.text

		#中身がselecter
		if type((sel:=myapp.curselecter.items[txt])) is Selecter:
			myapp.log.append(myapp.curselecter) #現を保存
			myapp.curselecter = sel
			get_app().layout = sel.layout
			get_app().layout.focus(sel.sel)

		#中身が関数等
		elif callable( (func:=myapp.curselecter.items[txt])):
			with StdoutRedirector(myapp.log[-1].label):
				func()

		#中身がテキスト
		else:
			myapp.curselecter.label.text=txt

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

