from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings

# フォーマット済みのテキスト
formatted_text = FormattedText([
    ('bold fg:green', 'Hello, '),
    ('italic fg:blue', 'world!'),
    ('', '\nThis is a styled text.')
])

bindings = KeyBindings()

@bindings.add('q')  # 'q'キーを終了キーとしてバインド
def exit_app(event):
	event.app.exit()

# FormattedTextControl を使ってテキストを表示
window = Window(content=FormattedTextControl(text=formatted_text))

# レイアウトに追加
root_container = HSplit([window])
layout = Layout(container=root_container)

# アプリケーションの作成
app = Application(
	layout=layout,
	full_screen=True,
	key_bindings=bindings,
)

# アプリケーションの実行
app.run()
