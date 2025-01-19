import traceback
from io import StringIO
import sys
import asyncio
import threading

from typing import Self,Any,Callable

from prompt_toolkit.application import Application
from prompt_toolkit.application import (
	get_app,
	get_app_or_none,
)
from prompt_toolkit.layout import (
	Layout,
	HSplit,
	Window,
	ScrollablePane,
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import (
	KeyBindings,
	merge_key_bindings,
	DynamicKeyBindings,
)
from prompt_toolkit.widgets import (
	Label,
	HorizontalLine,
	TextArea,
)



from .row import Row
from .stdoutredirector import StdoutRedirector

class Menu:
	"""
	Menuか関数をvalに持って、選択で実行する
	"""
	def __init__(
		self,
		items        : list[ tuple[ str,type[Self] | Callable[..., Any] ] ],      
		message      : str = "",
		console      : bool = True,
		)           -> None:
	
		self.base_items     = items   #基本となるｺﾏﾝﾄﾞ名とｺﾏﾝﾄﾞ
		self.display_items  = items   #表示用のｺﾏﾝﾄﾞ名とｺﾏﾝﾄﾞ
		self._message       = message #ｺﾝｿｰﾙ部に表示されるstrまたは表示を行う関数
		self.previous_menu  = None    #直前Menuのｲﾝｽﾀﾝｽ
		self._layout        = None    #基本となるLayout
		self.console        = console #関数のprint,returnを表示するか

		self._make_layout()           #基本layout作成

		#主となるコンテンツはtabで切り替えたい
		self.kb = [
			self._info_keys(),
			self._selecter_keys(),
		]
		
		self.mainindex = 1 #ｺﾝｿｰﾙ･選択部の切り替え
		self.rowindex  = 0 #選択肢の選択行

	def message_reset(self):
		"""
		情報を表示するｴﾘｱを初期状態に戻す
		関数も対応できるようにしたい
		"""
		if type(self._message) == str:
			self.console_area.text = self._message
		else:
			stdout = StdoutRedirector()
			with stdout:
				tail = self._message()

			if type(tail)==str:
				stdout.capture += tail

			self.console_area.text = stdout.capture

	#Layout{{{
	def _make_layout(self):
		"""
		layoutの初期化設定
		"""

		#self.display_items 　--[(name,val)...]の選択するｺﾝﾃﾝﾂ
		#self.rowlist         --選択肢の行のWindowﾘｽﾄ	
		self.display_items  = [("back",lambda:Command.back(self) ),] + self.base_items
		self.rowlist        = [Row(name) for name,val in self.display_items]

		#情報を表示するlayout
		self.console_area = TextArea(text="")

		self.info_area = HSplit([
			self.console_area,
			HorizontalLine(),
		])

		#選択肢だけのlayout
		self.command = HSplit(self.rowlist)
		self.command_area = ScrollablePane(self.command,height=10)

		#総合のlayout
		layout = HSplit(
			[self.info_area,self.command_area],
			key_bindings = DynamicKeyBindings(self.main_kb),
		)

		#出力表示しないなら切り替え
		if not self.console:		
			self.console_area.dont_extend_height = True
			self.command_area.height=None

		#self.layout --app上の構成
		self._layout = Layout(layout,focused_element=self.rowlist[0])

	@property
	def layout(self):
		"""
		app.layout = Menu.layout　で設定するときに再設定したいものを記述
		"""
		#self.console_area.text=self.message
		self.message_reset()
		return self._layout

	#}}}
		
	#keybind{{{
	def main_kb(self) -> KeyBindings:
		return merge_key_bindings([
			self._common_kb(),
			self.kb[self.mainindex],
		])

	def _common_kb(self) -> KeyBindings:
		kb = KeyBindings()

		@kb.add("tab")
		def _(event):
			"""
			console,commandのﾌｫｰｶｽ移動
			"""
			self.mainindex+=1
			if self.mainindex >= len(self.kb):
				self.mainindex = 0

			if self.mainindex == 0:
				event.app.layout.focus(self.info_area)
			elif self.mainindex == 1:
				event.app.layout.focus(self.rowlist[self.rowindex])

		@kb.add("escape", eager=True)
		def _(event):
			"""
			前Menuに戻るか、終了する
			"""
			if self.previous_menu != None:
				get_app().layout = self.previous_menu.layout
			else:
				event.app.exit()

		return kb

	def _info_keys(self) -> KeyBindings:
		kb = KeyBindings()
		
		return kb

	def _selecter_keys(self) -> KeyBindings:
		kb = KeyBindings()

		@kb.add("down")
		@kb.add("j")
		def _(event):
			self.rowindex+=1
			if self.rowindex >= len(self.rowlist):
				self.rowindex=0
			event.app.layout.focus(
				self.rowlist[self.rowindex]
			)

		@kb.add("up")
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

			select_item = self.display_items[self.rowindex][1]

			#中身がMenu
			if type( (select_menu:=select_item )) is type(self):
				select_menu.previous_menu = self
				get_app().layout = select_menu.layout

			#中身が関数等
			elif callable( (select_func:= select_item) ):
				#ｽﾚｯﾄﾞで裏側で起動する、menuの操作を継続して可能にして強制終了できる
				#selecter,inputerも関数扱い、メインスレッドのApplicationが止まると動作不能になる
				loop = asyncio.new_event_loop()
				thread1 = threading.Thread(target=self.task,args=(loop,select_func), daemon=True)
				thread1.start()
	
		return kb
	#}}}



	def task(self,loop,func):
		asyncio.set_event_loop(loop)
		loop.run_until_complete(self.execute(func))

	async def execute(self,func):
		"""
		選択した関数の実行を行う
		関数の標準出力はMenuのconsole_areaに出力
		"""

		if self.console:
			stdout = StdoutRedirector()
			tail=None

			with stdout:
				try:
					tail = func()
				except BaseException as e:
					print(traceback.format_exc())

			self.message_reset()                     #func後にmessageを更新(funcの更新内容を反映できる)
			self.console_area.text += stdout.capture #funcそのものの出力を更新
			if type(tail) == str:
				self.console_area.text += tail       #funcのreturnも文字表現可能なら更新

			get_app().invalidate()#再描画
		else:
			try:
				func()
			except:
				pass
			self.message_reset()

	def pre_run(self):
		"""
		起動時の調整
		ﾌｫｰｶｽ設定がLayoutのfocused_elementだとうまくいかない
		"""
		get_app().layout.focus(self.rowlist[0])

	def run(self):
		"""
		Application.run()を行う
		"""
		#ｺﾏﾝﾄﾞの更新
		self.rowlist[0]         = Row("exit")
		self.display_items[0]   = ("exit",Command.exit)
		self.command.children = [e.__pt_container__() for e in self.rowlist]

		self.app = Application(
			layout      = self.layout,
			full_screen = True,
		)

		self.app.run(pre_run=self.pre_run)
		#asyncio.run(self.run_async())

class Command:
	"""
	Menu内で利用できる関数の定義
	"""
	def exit():
		"""
		appの終了
		"""
		get_app().exit()

	#前のmenuに戻る
	def back(menu):
		"""
		前のMenuへの移動
		"""
		get_app().layout = menu.previous_menu.layout



