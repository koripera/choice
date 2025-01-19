from coa import Menu,selecter,inputer

def main():
	message = tx(
	"""
	-------------------
	This app supports the execution of functions.

	j , down : move down
	k , up   : mobe up  
	enter    : Run the item at the cursor
	escape   : Exit or previous menu
	-------------------
	"""
	)

	items = [
		("input & print"         , input_print ),
		("select & print"        , select_print),
		("Menu with many items"  , submenu()   ),
	]

	#Menu supports the following arguments: items and message
	main_menu = Menu(
		items   = items,
		message = message,
	)

	main_menu.run()

def submenu():

	items = [(i,"") for i in range(100)]

	message = "This is not a function or a menu, so selecting it will do nothing."

	menu = Menu(items,message,console=False)

	return menu



def input_print():
	message = "input the text and press Enter"

	inputed_string = inputer(message)
	print(inputed_string)
	return inputed_string

def select_print():
	"""
	items... list( tuple( name , func or Menu )... )
	"""
	items = [
		("aaa","aaa"),
		("iii","iii"),
		("uuu","uuu"),
	]

	message = "Select and press Enter"

	res = selecter(items,message)

	print( f"print in a function : {res}")
	return f"return value        : {res}"


def tx(txt):
	from textwrap import dedent
	return dedent(txt).strip() + "\n\n"

if __name__ == "__main__":
	main()
