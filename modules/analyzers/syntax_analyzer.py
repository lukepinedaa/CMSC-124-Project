import re

def parser(output):
	code_copy = output.copy()
	error = ""
	newArr = []
	newArr1 = []
	line_error = 0
	lineCheckCount = 0
	linecount = 0
	for lines in code_copy:
		for elements in lines:
			if elements.get("type") == "Comment Delimiter":
				lines.remove(elements)
	while [] in code_copy:
		code_copy.remove([])
	for lines in output:
		line = ""
		for elements in lines:
			if line == "":
				line = elements.get("lexeme")
			else:
				line += " " + elements.get("lexeme")
		newArr1.append(line)
	for lines in code_copy:
		line = ""
		for elements in lines:
			if line == "":
				line = elements.get("lexeme")
			else:
				line += " " + elements.get("lexeme")
		newArr.append(line)
	linecount = len(newArr)



	# VISIBLE varident, VISIBLE no troof literal, GIMMEH varident, I HAS A varident, I HAS A varident ITZ literal, I HAS A varident ITZ varident, varident R varident, 

	#VISIBLE regexs
	#VISIBLE varident and VISIBLE no troof literal
	VISIBLE1 = "^VISIBLE([^\S\r\n](-?(\d*\.\d+)|-?\d+|\".*\"|[a-zA-Z]\w*))+$"
	#VISIBLE non_bool_expr - <math_expr> | <concatenate_yarn> | maek <type_casting_operand> a type |  maek <type_casting_operand> type
	#<math_expr>
	VISIBLE2 = "^VISIBLE[^\S\r\n](SUM[^\S\r\n]OF|DIFF[^\S\r\n]OF|PRODUKT[^\S\r\n]OF|QUOSHUNT[^\S\r\n]OF|MOD[^\S\r\n]OF|BIGGR[^\S\r\n]OF|SMALLR[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	#comparisonexpr
	VISIBLE3 = "^VISIBLE[^\S\r\n](BOTH[^\S\r\n]SAEM|DIFFRINT)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]((BIGGR[^\S\r\n]OF|SMALLR[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n])?([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	#GIMMEH regexs
	#GIMMEH varident
	GIMMEH1 = "^GIMMEH[^\S\r\n][a-zA-Z]\w*$"
	#variable declaration regexs
	#I HAS A varident
	IHASA1 = "^(I[^\S\r\n]HAS[^\S\r\n]A)[^\S\r\n][a-zA-Z]\w*$"
	#I HAS A varident ITZ literal | I HAS A varident ITZ varident
	IHASA2 = "^(I[^\S\r\n]HAS[^\S\r\n]A)[^\S\r\n][a-zA-Z]\w*[^\S\r\n]ITZ[^\S\r\n](-?(\d*\.\d+)|-?\d+|\".*\"|[a-zA-Z]\w*|(WIN|FAIL))$"
	#I HAS A varident ITZ expr
	#<math_expr>
	IHASA3 = "^(I[^\S\r\n]HAS[^\S\r\n]A)[^\S\r\n][a-zA-Z]\w*[^\S\r\n]ITZ[^\S\r\n](SUM[^\S\r\n]OF|DIFF[^\S\r\n]OF|PRODUKT[^\S\r\n]OF|QUOSHUNT[^\S\r\n]OF|MOD[^\S\r\n]OF|BIGGR[^\S\r\n]OF|SMALLR[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	#comparison expr
	IHASA4 = "^(I[^\S\r\n]HAS[^\S\r\n]A)[^\S\r\n][a-zA-Z]\w*[^\S\r\n]ITZ[^\S\r\n](BOTH[^\S\r\n]SAEM|DIFFRINT)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]((BIGGR[^\S\r\n]OF|SMALLR[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n])?([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	#<bool_expr>
	#assignment regexs
	#varident R literal | varident R varident
	assign1 = "^[a-zA-Z]\w*[^\S\r\n]R[^\S\r\n](-?(\d*\.\d+)|-?\d+|\".*\"|[a-zA-Z]\w*|(WIN|FAIL))$"
	#varident R expr - <math_expr> | <comparison_expr> | <bool_expr> | <bool_expr_infinite> | <concatenate_yarn> | <type_casting>
	#varident R math_expr
	assign2 = "^[a-zA-Z]\w*[^\S\r\n]R[^\S\r\n](SUM[^\S\r\n]OF|DIFF[^\S\r\n]OF|PRODUKT[^\S\r\n]OF|QUOSHUNT[^\S\r\n]OF|MOD[^\S\r\n]OF|BIGGR[^\S\r\n]OF|SMALLR[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	#bool_expr
	assign3 = "^[a-zA-Z]\w*[^\S\r\n]R[^\S\r\n](BOTH[^\S\r\n]OF|EITHER[^\S\r\n]OF|WON[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	assign4 = "^[a-zA-Z]\w*[^\S\r\n]R[^\S\r\n]NOT[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	#comparison expr
	assign5 = "^[a-zA-Z]\w*[^\S\r\n]R[^\S\r\n](BOTH[^\S\r\n]SAEM|DIFFRINT)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]((BIGGR[^\S\r\n]OF|SMALLR[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n])?([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	#boolinf
	assign6 = "^[a-zA-Z]\w*[^\S\r\n]R[^\S\r\n](ALL[^\S\r\n]OF|ANY[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))([^\S\r\n]AN[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL)))*$"
	#typecast
	assign7 = "^[a-zA-Z]\w*[^\S\r\n]R[^\S\r\n]MAEK[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n](A[^\S\r\n])?(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)$"

	#math_expr (no nested functionality)
	math_expr = "^(SUM[^\S\r\n]OF|DIFF[^\S\r\n]OF|PRODUKT[^\S\r\n]OF|QUOSHUNT[^\S\r\n]OF|MOD[^\S\r\n]OF|BIGGR[^\S\r\n]OF|SMALLR[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"	
	#bool_expr (no nested functionality)
	bool_expr1 = "^(BOTH[^\S\r\n]OF|EITHER[^\S\r\n]OF|WON[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	bool_expr2 = "^NOT[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	#comparison_expr (no nested functionality)
	comp_expr1 = "^(BOTH[^\S\r\n]SAEM|DIFFRINT)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]((BIGGR[^\S\r\n]OF|SMALLR[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n])?([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	#boolinfexpr
	bool_inf_expr1 =  "^(ALL[^\S\r\n]OF|ANY[^\S\r\n]OF)[^\S\r\n]((BOTH[^\S\r\n]SAEM|DIFFRINT)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]((BIGGR[^\S\r\n]OF|SMALLR[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n])?([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))|[a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))([^\S\r\n]AN[^\S\r\n]((BOTH[^\S\r\n]SAEM|DIFFRINT)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]((BIGGR[^\S\r\n]OF|SMALLR[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n])?([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))|[a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL)))*$"
	#typcast
	typecast1 = "^MAEK[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n](A[^\S\r\n])?(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)$"
	typecast2 = "^[a-zA-Z]\w*[^\S\r\n]IS[^\S\r\n]NOW[^\S\r\n]A[^\S\r\n](TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)$"
	HAI = "^HAI ([0-9]*)(\.([0-9]+))?$"
	KTHXBYE = "^KTHXBYE$"
	O_RLY = "^O[^\S\r\n]RLY\?$"
	YA_RLY = "^YA[^\S\r\n]RLY$"
	WTF = "^WTF\?$"
	OMG_literal = "^OMG[^\S\r\n](-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	GTFO = "^GTFO$"
	OMGWTF = "^OMGWTF$"
	OIC = "^OIC$"
	NO_WAI = "^NO[^\S\r\n]WAI$"
	LOOP1 = "^IM[^\S\r\n]IN[^\S\r\n]YR[^\S\r\n][a-zA-Z]\w*[^\S\r\n](UPPIN|NERFIN)[^\S\r\n]YR[^\S\r\n][a-zA-Z]\w*[^\S\r\n]((TIL|WILE)[^\S\r\n])?(BOTH[^\S\r\n]SAEM|DIFFRINT)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n]((BIGGR[^\S\r\n]OF|SMALLR[^\S\r\n]OF)[^\S\r\n]([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))[^\S\r\n]AN[^\S\r\n])?([a-zA-Z]\w*|-?(\d*\.\d+)|-?\d+|\".*\"|(WIN|FAIL))$"
	LOOP2 = "^IM[^\S\r\n]OUTTA[^\S\r\n]YR[^\S\r\n][a-zA-Z]\w*$"
	regexpatterns = [VISIBLE3, VISIBLE2,VISIBLE1, GIMMEH1, IHASA1, IHASA2, IHASA3, IHASA4, assign1,assign2,assign3,assign4,assign5,assign6,assign7, math_expr, bool_expr1, bool_expr2, comp_expr1, bool_inf_expr1, typecast1, typecast2, O_RLY, WTF, OMG_literal, GTFO, OMGWTF, OIC, YA_RLY,NO_WAI, LOOP1, LOOP2]
	


	if re.match(HAI, newArr[0]):
		lineCheckCount +=1
	else:
		error = "HAI missing"
		for lines in range(len(output)):
			if newArr[0] == newArr1[lines]:
				line_error = lines+1
				break
		print("Line:",line_error, "\n",error)
		return(line_error, error)
	if re.match(KTHXBYE, newArr[-1]):
		pass
	else:
		error = "KTHXBYE missing"
		for lines in range(len(output)):
			if newArr[-1] == newArr1[lines]:
				line_error = lines+1
				break
		print("Line:",line_error, "\n",error)
		return(line_error, error)

	while lineCheckCount < linecount-1 and lineCheckCount != 0:
		noerror = False
		curr_line = newArr[lineCheckCount]
		for regex in regexpatterns:
			reg = regex
			if re.match(reg,curr_line):
				noerror = True
				break
			elif regex == regexpatterns[-1]:
				print(curr_line)
				print("wala pa sa syntax")
			else:
				continue



		if noerror == True:
			lineCheckCount+=1
			continue
		else:
			error = "Syntax Error"
			for lines in range(len(output)):
				if newArr[lineCheckCount] == newArr1[lines]:
					line_error = lines+1
					break
			print("Line:",line_error, "\n",error)
			return(line_error, error)

	return(line_error, error)