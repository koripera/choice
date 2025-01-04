import prompt_toolkit

#色やｽﾀｲﾙを指定した文字列を作成する
txt = prompt_toolkit.formatted_text.FormattedText((
("#FF0000","xxxxxxxxxx"),
("#FFA500","xxxxxxxxxx"),
("#FFFF00","xxxxxxxxxx"),
("#008000","xxxxxxxxxx"),
("#00FFFF","xxxxxxxxxx"),
("#0000FF","xxxxxxxxxx"),
("#800080","xxxxxxxxxx"),
))

#ｽﾀｲﾙ指定の文字列をprintする
prompt_toolkit.print_formatted_text(txt)
