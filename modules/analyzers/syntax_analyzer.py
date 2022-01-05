def parser(output):
	line_check_count = 0
	symbol_table = {}
	output_copy = output.copy()
	error = ""
	line = 0
	line_error = 0
	for lines in output:
		for elements in lines:
			if elements.get("type") == "Comment Delimiter":
				lines.remove(elements)
	while [] in output:
		output.remove([])

	for lines in output_copy:
		for elements in lines:
			if elements.get("type") == "Comment Delimiter":
				lines.remove(elements)
	linecount = len(output)
	linecount1 = len(output_copy)



	if output[0][0].get("lexeme") == "HAI" :
		line_check_count +=1
		line =0 
	else:

		for elements in range(linecount1-1):
			if output[line] == output_copy[elements]:
				line_error = elements + 1
		error = "Syntax Error: Code Delimiter Missing"
		print("Line:", line_error, error)
		return(line_error,error, symbol_table)
	if output[linecount-1][0].get("lexeme") == "KTHXBYE":
		line = linecount - 1
	else:
		for elements in range(linecount1-1):
			if output[line] == output_copy[elements]:
				line_error = elements+1
		error = "Syntax Error: Code Delimiter Missing"
		print("Line:", line_error, error)
		return(line_error,error, symbol_table)
	startloop = 0
	loopident = ""
	while line_check_count < linecount-1 and line_check_count != 0:

		isVarDec = 0
		varID = ""
		has_itz = 0
		error = ""
		is_operator = 0
		isLiteral = 0
		isVarID = 0
		literal_type = ""
		isPrint = 0
		hasR = 0
		expression = ""
		hasAn = 0
		operator_count = 0
		an_count = 0
		isRecast = 0
		gimmeh = 0
		math_expr = 0
		bool_expr = 0
		bool_expr_inf = 0
		cnt = 0
		notcnt = 0
		not_count =0
		cmpr_expr = 0
		indec = ""
		connector = 0
		loop = 0
		endloop = 0
		concat = 0
		typecast = 0
		once = 0
		for lexemes in range(len(output[line_check_count])):
			# checks if the current lexeme is a vardec
			# lines 33 - 46 - i has a varident
			if output[line_check_count][lexemes].get("type") == "Line Delimiter":
				continue

			elif output[line_check_count][lexemes].get("type") == "Variable Declaration" and isVarDec == 0:
				isVarDec = 1
				continue
			#if the previous lexeme is a vardec, the current lexeme is the key (variable)
			elif isVarDec == 1 and isVarID == 0 and output[line_check_count][lexemes].get("type") == "Variable Identifier":
				varID = output[line_check_count][lexemes].get("lexeme")
				
				isVarID = 1
				#if the current lexeme is the last on a line, set value to NOOB and saves the key and value to the symbol table
				if lexemes == len(output[line_check_count])-1:
					key = varID
					value = "NOOB"
					symbol_table[key] = value
					isVarDec = 0
				continue
			#if the previous lexeme is varid, checks if the current lexeme is the ITZ keyword 
			# lines 33 - 77 - i has a varident itz <literal>
			elif isVarID == 1 and has_itz ==0 and output[line_check_count][lexemes].get("type") == "Variable Assignment":
				has_itz = 1
				continue
			#if the lexeme after the ITZ keyword is a literal, saves the key and value to the symbol table
			elif has_itz == 1 and is_operator == 0  and lexemes == len(output[line_check_count])-1 and (output[line_check_count][lexemes].get("type") == "Float Literal" or output[line_check_count][lexemes].get("type") == "Integer Literal" or output[line_check_count][lexemes].get("type") == "String Literal" or output[line_check_count][lexemes].get("type") == "Boolean Literal"):
				literal_type = output[line_check_count][lexemes].get("type")
				if literal_type == "Float Literal":
					key = varID
					value = float(output[line_check_count][lexemes].get("lexeme"))
					symbol_table[key] = value
				elif literal_type == "Integer Literal":
					key = varID
					value = int(output[line_check_count][lexemes].get("lexeme"))
					symbol_table[key] = value
				elif literal_type == "String Literal":
					key = varID
					value = output[line_check_count][lexemes].get("lexeme")
					symbol_table[key] = value[1:-1]
				else:
				 	key = varID
				 	value = output[line_check_count][lexemes].get("lexeme")
				 	symbol_table[key] = value
				continue
			#if the lexeme after the ITZ keyword is an arithmetic operator, saves the operator and the whole expression in one variable
			#lines 33 - n - i has varident itz <expr>/ varident R <varident> / varident R <literal> / varident R <expr> / visible varident | visible <non_bool_expr> | visible <no_troof_literal>
			#lines 81 - 120 <math_expr>
			elif is_operator == 0 and (output[line_check_count][lexemes].get("type") == "Addition Operator" or output[line_check_count][lexemes].get("type") == "Subtraction Operator" or output[line_check_count][lexemes].get("type") == "Product Operator" or output[line_check_count][lexemes].get("type") == "Quotient Operator" or output[line_check_count][lexemes].get("type") == "Modulo Operator" or output[line_check_count][lexemes].get("type") == "Max Operator" or output[line_check_count][lexemes].get("type") == "Min Operator" ):
				math_expr = 1
				operator_count +=1
				operator = output[line_check_count][lexemes].get("type")
				is_operator = 1
				if expression == "":
					expression = output[line_check_count][lexemes].get("lexeme")
				else:
					expression += " " + output[line_check_count][lexemes].get("lexeme")
				continue
			elif (is_operator == 1 or hasAn == 1) and (math_expr == 1 or bool_expr_inf == 1 or cmpr_expr == 1) and (output[line_check_count][lexemes].get("type") == "Addition Operator" or output[line_check_count][lexemes].get("type") == "Subtraction Operator" or output[line_check_count][lexemes].get("type") == "Product Operator" or output[line_check_count][lexemes].get("type") == "Quotient Operator" or output[line_check_count][lexemes].get("type") == "Modulo Operator" or output[line_check_count][lexemes].get("type") == "Max Operator" or output[line_check_count][lexemes].get("type") == "Min Operator" ):
				expression = expression + " " + output[line_check_count][lexemes].get("lexeme")
				operator_count +=1
				cnt += 1	
				if hasAn == 1:
					hasAn = 0
				continue	
			elif is_operator == 1 and hasAn == 0 and (math_expr == 1 or bool_expr_inf == 1 or cmpr_expr == 1) and (output[line_check_count][lexemes].get("type") == "Float Literal" or output[line_check_count][lexemes].get("type") == "Integer Literal" or  output[line_check_count][lexemes].get("type") == "Variable Identifier" or  output[line_check_count][lexemes].get("type") == "String Literal"):
				
				expression = expression + " " + output[line_check_count][lexemes].get("lexeme")
				cnt += 1
				if operator == "Not Operator":
					not_count +=1
				if operator == "Not Operator" and lexemes == len(output[line_check_count])-1:
					if (has_itz == 1 or hasR == 1):	
						if notcnt == not_count:
							key = varID
							value = expression
							symbol_table[key] = value
							continue
						else:
							for elements in range(linecount1-1):
								if output[line_check_count] == output_copy[elements]:
									line_error = elements+1
							error = "Syntax Error: Invalid Expression"
							print("Line:", line_error, error)
							return(line_error,error, symbol_table)
					if isPrint == 1:
						if notcnt == not_count: 
							continue
						else:
							for elements in range(linecount1-1):
								if output[line_check_count] == output_copy[elements]:
									line_error = elements+1
							error = "Syntax Error: Invalid Expression"
							print("Line:", line_error, error)
							return(line_error,error, symbol_table)
				continue
			elif is_operator == 1 and (output[line_check_count][lexemes].get("type") == "Operand Separator"):
				an_count += 1
				hasAn = 1
				expression = expression + " " + output[line_check_count][lexemes].get("lexeme")
				if lexemes == len(output[line_check_count])-1:
					for elements in range(linecount1-1):
						if output[line_check_count] == output_copy[elements]:
							line_error = elements+1
					error = "Syntax Error: Invalid Expression"
					print("Line:", line_error, error)
					return(line_error,error, symbol_table)
				continue
			elif hasAn == 1 and (math_expr == 1 or bool_expr_inf == 1 or cmpr_expr == 1) and (output[line_check_count][lexemes].get("type") == "Float Literal" or output[line_check_count][lexemes].get("type") == "Integer Literal" or  output[line_check_count][lexemes].get("type") == "Variable Identifier" or  output[line_check_count][lexemes].get("type") == "String Literal"):
				
				expression = expression + " " + output[line_check_count][lexemes].get("lexeme")
				hasAn = 0
				cnt += 1
				if (has_itz == 1 or hasR == 1):
					if math_expr ==1 or cmpr_expr == 1:	
						if lexemes == len(output[line_check_count])-1:

							if operator_count == an_count:
								key = varID
								value = expression
								symbol_table[key] = value
								continue
							else:
								for elements in range(linecount1-1):
									if output[line_check_count] == output_copy[elements]:
										line_error = elements+1
								error = "Syntax Error: Invalid Expression"
								print("Line:", line_error, error)
								return(line_error,error, symbol_table)
					elif bool_expr_inf == 1:
						if lexemes == len(output[line_check_count])-1 or output[line_check_count][lexemes+1].get("type") == "Line Delimiter":
							if an_count == cnt-1:
								key = varID
								value = expression
								symbol_table[key] = value
								continue
							else:
								for elements in range(linecount1-1):
									if output[line_check_count] == output_copy[elements]:
										line_error = elements+1
								error = "Syntax Error: Invalid Expression"
								print("Line:", line_error, error)
								return(line_error,error, symbol_table)
				
				if isPrint == 1:
					if math_expr == 1 or cmpr_expr == 1:
						if lexemes == len(output[line_check_count])-1 :
							if operator_count == an_count:
								continue
							else:
								for elements in range(linecount1-1):
									if output[line_check_count] == output_copy[elements]:
										line_error = elements+1
								error = "Syntax Error: Invalid Expression"
								print("Line:", line_error, error)
								return(line_error,error, symbol_table)
					elif bool_expr_inf == 1:
						if lexemes == len(output[line_check_count])-1 or output[line_check_count][lexemes+1].get("type") == "Line Delimiter":
							if an_count == cnt-1:
								continue
							else:
								for elements in range(linecount1-1):
									if output[line_check_count] == output_copy[elements]:
										line_error = elements+1
								error = "Syntax Error: Invalid Expression"
								print("Line:", line_error, error)
								return(line_error,error, symbol_table)
				continue
			#lines 122 - 162 <bool_expr>
			elif (output[line_check_count][lexemes].get("type") == "And Operator" or output[line_check_count][lexemes].get("type") == "Or Operator" or output[line_check_count][lexemes].get("type") == "XOR Operator" or output[line_check_count][lexemes].get("type") == "Not Operator"):
				bool_expr = 1
				operator = output[line_check_count][lexemes].get("type")
				operator_count +=1
				is_operator = 1
				if expression == "":
					expression = output[line_check_count][lexemes].get("lexeme")
				else:
					expression += " " + output[line_check_count][lexemes].get("lexeme")
				if operator == "Not Operator":
					notcnt +=1
				continue
			elif (is_operator == 1 or hasAn == 1) and (bool_expr == 1 or bool_expr_inf == 1 or cmpr_expr == 1) and (output[line_check_count][lexemes].get("type") == "And Operator" or output[line_check_count][lexemes].get("type") == "Or Operator" or output[line_check_count][lexemes].get("type") == "XOR Operator" or output[line_check_count][lexemes].get("type") == "Not Operator"):
				
				expression = expression + " " + output[line_check_count][lexemes].get("lexeme")
				operator = output[line_check_count][lexemes].get("type")
				operator_count +=1
				cnt += 1
			
				if hasAn == 1:
					hasAn = 0
				if operator == "Not Operator":
					hasAn = 0
					notcnt += 1
				continue	
			elif is_operator == 1 and hasAn == 0 and (bool_expr == 1 or bool_expr_inf == 1 or cmpr_expr == 1) and (output[line_check_count][lexemes].get("type") == "Float Literal" or output[line_check_count][lexemes].get("type") == "Integer Literal" or  output[line_check_count][lexemes].get("type") == "Variable Identifier" or output[line_check_count][lexemes].get("type") == "String Literal" or output[line_check_count][lexemes].get("type") == "Boolean Literal"):
				
				expression = expression + " " + output[line_check_count][lexemes].get("lexeme")
				cnt += 1
				if operator == "Not Operator":
					not_count +=1
				if operator == "Not Operator" and lexemes == len(output[line_check_count])-1:
					if (has_itz == 1 or hasR == 1):	
						if notcnt == not_count:
							key = varID
							value = expression
							symbol_table[key] = value
							continue
						else:
							for elements in range(linecount1-1):
								if output[line_check_count] == output_copy[elements]:
									line_error = elements+1
							error = "Syntax Error: Invalid Expression"
							print("Line:", line_error, error)
							return(line_error,error, symbol_table)
					if isPrint == 1:
						if notcnt == not_count: 
							continue
						else:
							for elements in range(linecount1-1):
								if output[line_check_count] == output_copy[elements]:
									line_error = elements+1
							error = "Syntax Error: Invalid Expression"
							print("Line:", line_error, error)
							return(line_error,error, symbol_table)
				continue 
			elif hasAn == 1 and (bool_expr == 1 or bool_expr_inf == 1 or cmpr_expr == 1) and (output[line_check_count][lexemes].get("type") == "Float Literal" or output[line_check_count][lexemes].get("type") == "Integer Literal" or  output[line_check_count][lexemes].get("type") == "Variable Identifier" or output[line_check_count][lexemes].get("type") == "String Literal" or output[line_check_count][lexemes].get("type") == "Boolean Literal"):
				
				expression = expression + " " + output[line_check_count][lexemes].get("lexeme")
				hasAn = 0
				cnt += 1
				if (has_itz == 1 or hasR == 1):
					if bool_expr ==1 or cmpr_expr == 1:	
						if lexemes == len(output[line_check_count])-1:

							if operator_count == an_count:
								key = varID
								value = expression
								symbol_table[key] = value
								continue
							else:
								for elements in range(linecount1-1):
									if output[line_check_count] == output_copy[elements]:
										line_error = elements+1
								error = "Syntax Error: Invalid Expression"
								print("Line:", line_error, error)
								return(line_error,error, symbol_table)
					elif bool_expr_inf == 1:
						if lexemes == len(output[line_check_count])-1 or output[line_check_count][lexemes+1].get("type") == "Line Delimiter":
							if an_count == cnt-1:
								key = varID
								value = expression
								symbol_table[key] = value
								continue
							else:
								for elements in range(linecount1-1):
									if output[line_check_count] == output_copy[elements]:
										line_error = elements+1
								error = "Syntax Error: Invalid Expression"
								print("Line:", line_error, error)
								return(line_error,error, symbol_table)
				
				if isPrint == 1:
					if bool_expr == 1 or cmpr_expr == 1:
						if lexemes == len(output[line_check_count])-1:
							if operator_count == an_count: 
								continue
							else:
								for elements in range(linecount1-1):
									if output[line_check_count] == output_copy[elements]:
										line_error = elements+1
								error = "Syntax Error: Invalid Expression"
								print("Line:", line_error, error)
								return(line_error,error, symbol_table)
					elif bool_expr_inf == 1:
						if lexemes == len(output[line_check_count])-1 or output[line_check_count][lexemes+1].get("type") == "Line Delimiter":
							if an_count == cnt-1:
								continue
							else:
								for elements in range(linecount1-1):
									if output[line_check_count] == output_copy[elements]:
										line_error = elements+1
								error = "Syntax Error: Invalid Expression"
								print("Line:", line_error, error)
								return(line_error,error, symbol_table)
				continue
			#lines 164 - n <bool_expr_infinite>
			elif (output[line_check_count][lexemes].get("type") == "Infinite Arity Or Operator" or output[line_check_count][lexemes].get("type") == "Infinite Arity And Operator"):
				bool_expr_inf = 1
				operator_count +=1
				is_operator = 1
				operator = output[line_check_count][lexemes].get("type")
				if expression == "":
					expression = output[line_check_count][lexemes].get("lexeme")
				else:
					expression += " " + output[line_check_count][lexemes].get("lexeme")
				continue
			#line 350 - <comparison_expr>
			elif (output[line_check_count][lexemes].get("type") == "Equality Operator" or output[line_check_count][lexemes].get("type") == "Inequality Operator"):
				cmpr_expr = 1
				is_operator = 1
				operator_count +=1
				operator = output[line_check_count][lexemes].get("type")
				if expression == "":
					expression = output[line_check_count][lexemes].get("lexeme")
				else:
					expression += " " + output[line_check_count][lexemes].get("lexeme")
				continue

			#checks if the lexeme is the VISIBLE keyword, sets isPrint to 1
			elif output[line_check_count][lexemes].get("type") == "Output Keyword":
				isPrint = 1
				continue
			#if the previous lexeme is the VISIBLE keyword, print the current lexeme
			
			elif isPrint == 1 and output[line_check_count][lexemes].get("type") == "Variable Identifier" or output[line_check_count][lexemes].get("type") == "String Literal":
				
				continue
			elif isVarID == 0 and output[line_check_count][lexemes].get("type") == "Variable Identifier" and hasR == 0 and startloop == 0 and is_operator == 0:
				
				varID = output[line_check_count][lexemes].get("lexeme")
				isVarID = 1
				continue
			elif isVarID == 1 and hasR == 0 and output[line_check_count][lexemes].get("type") == "Assignment Keyword":
				hasR = 1
				continue
			elif hasR == 1 and (output[line_check_count][lexemes].get("type") == "Variable Identifier" or output[line_check_count][lexemes].get("type") == "Float Literal" or output[line_check_count][lexemes].get("type") == "Integer Literal" or output[line_check_count][lexemes].get("type") == "String Literal" or output[line_check_count][lexemes].get("type") == "Boolean Literal"):
				if output[line_check_count][lexemes].get("type") == "Variable Identifier":
					symbol_table[varID] = output[line_check_count][lexemes].get("type") == "Variable Identifier"
				elif output[line_check_count][lexemes].get("type") == "Float Literal":
					symbol_table[varID] = float(output[line_check_count][lexemes].get("lexeme"))
				elif output[line_check_count][lexemes].get("type") == "Integer Literal":
					symbol_table[varID] = int(output[line_check_count][lexemes].get("lexeme"))
				elif output[line_check_count][lexemes].get("type") == "String Literal":
					symbol_table[varID] = output[line_check_count][lexemes].get("lexeme")
				elif output[line_check_count][lexemes].get("type") == "Boolean Literal":
					if output[line_check_count][lexemes].get("lexeme") == "WIN":
						symbol_table[varID] = True
					elif output[line_check_count][lexemes].get("lexeme") == "FAIL" :
						symbol_table[varID] = False
					else:
						for elements in range(linecount1-1):
							if output[line_check_count] == output_copy[elements]:
								line_error = elements+1
						error = "Syntax Error: Invalid Expression"
						print("Line:", line_error, error)
						return(line_error,error, symbol_table)
						
				else:
					for elements in range(linecount1-1):
						if output[line_check_count] == output_copy[elements]:
							line_error = elements+1
					error = "Syntax Error: Invalid Expression"
					print("Line:", line_error, error)
					return(line_error,error, symbol_table)
					continue
			elif output[line_check_count][lexemes].get("type") == "Input Keyword":
				gimmeh = 1
				continue
			elif gimmeh == 1 and output[line_check_count][lexemes].get("type") == "Variable Identifier":
				continue
			elif isVarID == 1 and output[line_check_count][lexemes].get("type") == "Recast Operator":
				isRecast = 1
				continue
			elif isRecast == 1 and output[line_check_count][lexemes].get("type") == "Type Literal":
				continue
			elif output[line_check_count][lexemes].get("type") == "Start Loop Keyword":

				startloop = 1
				continue
			elif startloop == 1 and loopident == "" and output[line_check_count][lexemes].get("type") == "Variable Identifier":

				loopident = output[line_check_count][lexemes].get("lexeme")
				continue
			elif startloop == 1 and loopident != ""  and (output[line_check_count][lexemes].get("type") == "Increment Keyword" or output[line_check_count][lexemes].get("type") == "Decrement Keyword"):
				indec = output[line_check_count][lexemes].get("lexeme")
				continue
			elif startloop == 1 and loopident != "" and indec != "" and (output[line_check_count][lexemes].get("type") == "Connector Keyword"):
				connector = 1
				continue
			elif startloop == 1 and loopident != "" and indec != "" and connector == 1 and (output[line_check_count][lexemes].get("type") == "Variable Identifier"):

				isVarID = 1
				continue
			elif startloop == 1 and loopident != "" and indec != "" and connector == 1 and isVarID == 1 and output[line_check_count][lexemes].get("type") == "Loop Keyword":
				loop = 1 
				continue
			elif startloop == 1 and lexemes == 0 and output[line_check_count][lexemes].get("type") == "End Loop Keyword":
				endloop = 1
				continue
			elif endloop ==  1 and output[line_check_count][lexemes].get("lexeme") == loopident:
				startloop = 0
				loopident = ""
				continue
			elif output[line_check_count][lexemes].get("type") == "Concatenate Operator":
				concat = 1
				is_operator = 1
				operator_count +=1
				operator = output[line_check_count][lexemes].get("type")
				if expression == "":
					expression = output[line_check_count][lexemes].get("lexeme")
				else:
					expression += " " + output[line_check_count][lexemes].get("lexeme")
				continue
			elif concat == 1 and (output[line_check_count][lexemes].get("type") == "Variable Identifier" or output[line_check_count][lexemes].get("type") == "Float Literal" or output[line_check_count][lexemes].get("type") == "Integer Literal" or output[line_check_count][lexemes].get("type") == "String Literal" ):
				
				expression += " " + output[line_check_count][lexemes].get("lexeme")
				cnt +=1

				if lexemes == len(output[line_check_count])-1 or output[line_check_count][lexemes+1].get("type") == "Line Delimiter":
					if has_itz == 1 or hasR == 1:
						if cnt == an_count+1:
							key = varID
							value = expression
							symbol_table[key] =value
							continue
						else:
							for elements in range(linecount1-1):
								if output[line_check_count] == output_copy[elements]:
									line_error = elements+1	
							error = "Syntax Error"
							print("Line:", line_error, error)
							return(line_error,error, symbol_table)
					elif isPrint == 1:
						if cnt == an_count-1:
							continue
						else:
							for elements in range(linecount1-1):
								if output[line_check_count] == output_copy[elements]:
									line_error = elements+1	
							error = "Syntax Error"
							print("Line:", line_error, error)
							return(line_error,error, symbol_table)
					else:
						continue
				continue
			elif output[line_check_count][lexemes].get("type") == "Typecast Operator":
				typecast=1
				is_operator = 1
				operator = output[line_check_count][lexemes].get("lexeme")
				expression = output[line_check_count][lexemes].get("lexeme")

				continue
			elif typecast == 1 and is_operator == 1 and expression==operator and (output[line_check_count][lexemes].get("type") == "Variable Identifier" or output[line_check_count][lexemes].get("type") == "Float Literal" or output[line_check_count][lexemes].get("type") == "Integer Literal" or output[line_check_count][lexemes].get("type") == "String Literal" or output[line_check_count][lexemes].get("type") == "Boolean Literal"):
				

				expression += " " + output[line_check_count][lexemes].get("lexeme")
				if output[line_check_count][lexemes].get("type") == "Variable Identifier":
					varID = output[line_check_count][lexemes].get("lexeme")
				once += 1
				continue
			elif typecast == 1 and is_operator == 1 and expression != operator and output[line_check_count][lexemes].get("type") == "Separator":
				
				expression += " " + output[line_check_count][lexemes].get("lexeme")
				continue
			elif typecast == 1 and is_operator == 1 and expression != operator and output[line_check_count][lexemes].get("type") == "Type Literal":
				expression += " " + output[line_check_count][lexemes].get("lexeme")
				if lexemes == len(output[line_check_count])-1 and once == 1:
					if hasR == 1:
						key = varID
						value = expression
						symbol_table[key] = value
						continue
					elif isPrint == 1:
						continue
				else:
					for elements in range(linecount1-1):
						if output[line_check_count] == output_copy[elements]:
							line_error = elements+1	
					error = "Syntax Error"
					print("Line:", line_error, error)
					return(line_error,error, symbol_table)

				continue
			else:
				print(output[line_check_count][lexemes])
				for elements in range(linecount1-1):
					if output[line_check_count] == output_copy[elements]:
						line_error = elements+1	
				error = "Syntax Error"
				print("Line:", line_error, error)
				return(line_error,error, symbol_table)

		line_check_count+=1
		
	print("SYMBOL TABLE")
	for elements in symbol_table:
		print(elements,":", symbol_table[elements])
	return(line_error,error, symbol_table)


