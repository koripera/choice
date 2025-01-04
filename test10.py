from test9 import selecter

x=["a","b","c"]
y={
	"a":100,
	"b":lambda:selecter(["1","2","3","4"])
}

print(selecter(y))
