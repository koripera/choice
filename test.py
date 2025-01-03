from prompt_toolkit import Application
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.layout import Layout, HSplit
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

# 表示する複数行の文字列
text = "".join([f"line {e}\n" for e in range(10)])

style = Style.from_dict({
    'selected-line': 'bg:#4444ff #ffffff',  # 青背景に白文字
    'line': 'bg:#000000 #ffffff',           # 黒背景に白文字
})

# TextAreaウィジェットを作成
text_area = TextArea(
    text=text,        # 複数行の文字列を渡す
    read_only=True,   # 編集不可に設定
    scrollbar=True    # スクロールバーを表示
)

# 選択されている行のインデックス
selected_line = [0]

# レイアウトを設定
layout = Layout(HSplit([text_area]))

# キーバインディングを作成
bindings = KeyBindings()

def render_lines():
    text_fragments = []
    for i, line in enumerate(text.split("\n")):
        if i == selected_line[0]:
            text_fragments.append(('class:selected-line', line + '\n'))
        else:
            text_fragments.append(('class:line', line + '\n'))
    print(FormattedText(text_fragments))
    return FormattedText(text_fragments) 

@bindings.add('q')  # 'q'キーを終了キーとしてバインド
def exit_app(event):
    """アプリケーションを終了する"""
    event.app.exit()

@bindings.add('down')
def move_down(event):
    """下矢印キーで選択行を下に移動"""
    if selected_line[0] < len(text.split("\n")) - 1:
        selected_line[0] += 1
    text_area.text=render_lines()

# アプリケーションを構築
app = Application(
    layout=layout,
    style=style,
	key_bindings=bindings,
    full_screen=1  # 全画面表示
)

# アプリケーションを実行
if __name__ == "__main__":
    app.run()

