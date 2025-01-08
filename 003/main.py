from sub import Selecter


def aiueo():
	print("hello")
	print(input("aaa"))

a = Selecter({
	"aaa":"aaa",
	"iii":"iii",
	"uuu":"uuu",
	"aiueo":aiueo,
})

a.run()
