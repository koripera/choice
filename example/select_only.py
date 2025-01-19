from coa import selecter

def main():
	message = "aaa"

	res = selecter([
		("aaa","aaa"),
		("iii","iii"),
		("uuu","uuu"),
	])

	res2 = selecter([
		("aaa","aaa"),
		("iii","iii"),
		("uuu","uuu"),
	],
	message=message)

	print(res)
	print(res2)

if __name__ == "__main__":
	main()
