from sub import Selecter


def aiueo():
	print("hello")

	return "aaaa"

a = Selecter({
	"aaa":"aaa",
	"iii":"iii",
	"uuu":"uuu",
	"aiueo":aiueo,
})

a.run()
