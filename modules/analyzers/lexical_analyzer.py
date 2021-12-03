import re

#Converts string to sequence of tokens
def lexer(code):
    #keywords of more than one word (unique first word)
    flaggedWords = {"I": ["HAS", "A"], "SUM": ["OF"], "DIFF": ["OF"], "PRODUKT": ["OF"], "QUOSHUNT": ["OF"], "MOD": ["OF"], "BIGGR": ["OF"], "SMALLR": ["OF"], "EITHER": ["OF"], "WON": ["OF"], "ANY": ["OF"], "ALL": ["OF"], "IS": ["NOW", "A"], "O": ["RLY?"], "YA": ["RLY"], "NO": ["WAI"]}
    #keywords of more than one word (nonunique first word)
    flaggedWords2 = {"BOTH": [["OF"], ["SAEM"]], "IM": [["IN", "YR"], ["OUTTA", "YR"]]}

    #regex with their respective type
    regexPatterns = {"^-?(\d*\.\d+)$":"Float Literal", "^-?\d+$":"Integer Literal", "^\".*\"$": "String Literal", "^(WIN|FAIL)$":"Boolean Literal", "^(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)$":"Type Literal", "^HAI$":"Code Delimiter", "^KTHXBYE$":"Code Delimiter", "^(I[^\S\r\n]HAS[^\S\r\n]A)$": "Variable Declaration", "^ITZ$":"Variable Assignment", "^R$":"Assignment Keyword", "^(SUM[^\S\r\n]OF)$":"Addition Operator", "^(DIFF[^\S\r\n]OF)$":"Subtraction Operator", "^(PRODUKT[^\S\r\n]OF)$":"Product Operator", "^(QUOSHUNT[^\S\r\n]OF)$":"Quotient Operator", "^(MOD[^\S\r\n]OF)$":"Modulo Operator", "^(BIGGR[^\S\r\n]OF)$":"Max Operator", "^(SMALLR[^\S\r\n]OF)$":"Min Operator", "^(BOTH[^\S\r\n]OF)$":"And Operator", "^(EITHER[^\S\r\n]OF)$":"Or Operator", "^(WON[^\S\r\n]OF)$":"XOR Operator", "^NOT$":"Not Operator", "^(ANY[^\S\r\n]OF)$":"Infinite Arity Or Operator", "^(ALL[^\S\r\n]OF)$":"Infinite Arity And Operator", "^(BOTH[^\S\r\n]SAEM)$":"Equality Operator", "^DIFFRINT$":"Inequality Operator", "^SMOOSH$":"Concatenate Operator", "^MAEK$":"Typecast Operator", "^A$":"Separator", "^(IS[^\S\r\n]NOW[^\S\r\n]A)$":"Recast Operator", "^VISIBLE$":"Output Keyword", "^GIMMEH$":"Input Keyword", "^O[^\S\r\n]RLY\?$":"Conditional Delimiter", "^(YA[^\S\r\n]RLY)$":"If Keyword", "^MEBBE$":"Else If Keyword", "^(NO[^\S\r\n]WAI)$":"Else Keyword", "^OIC$":"Conditional Delimiter", "^WTF\?$":"Conditional Delimiter", "^OMG$":"Case Keyword", "^OMGWTF$":"Default Case Keyword", "^(IM[^\S\r\n]IN[^\S\r\n]YR)$":"Start Loop Keyword", "^UPPIN$":"Increment Keyword", "^NERFIN$":"Decrement Keyword", "^YR$":"Connector Keyword", "^TIL$":"Loop Keyword", "^WILE$":"Loop Keyword", "^(IM[^\S\r\n]OUTTA[^\S\r\n]YR)$":"End Loop Keyword", "AN":"Operand Separator", "MKAY": "Line Delimiter", "GTFO": "Break Keyword", "^[a-zA-Z]\w*$":"Variable Identifier"}

    #list that will serve as the symbol table
    symbolTable = []

    obtw = False #obtw comment flag

    #split code with new line as delimiter
    lines = code.splitlines()

    #get the lexemes per line
    for lineCounter in range (len(lines)):

        #keep the delimiter when using re.split() : https://stackoverflow.com/questions/2136556/in-python-how-do-i-split-a-string-and-keep-the-separators
        #split line with string literal regex as delimiter
        tempList = re.split(r'(["][^"]*["])', lines[lineCounter])
        
        #list that will hold the "words" in current line
        words = []
        for i in range (0, len(tempList)):
            #current element is a string literal, append to words as it is
            if re.match(r'["][^"]*["]', tempList[i]):
                words.append(tempList[i])
            #concatenate words and string split result
            else:
                words += tempList[i].split()
        
        #set skip to 0 and currentLine to empty list
        skip, currentLine = 0, []

        #access every element in words
        for i in range (0, len(words)):
            #assign current words element to lexeme variable
            lexeme = words[i]

            #skip words because word is already concatenated to some prev word
            if skip > 0: 
                skip -= 1
                continue

            #ignore comments, return errors if found
            if (words[i] == "BTW") or (words[i] == "OBTW") or (words[i] == "TLDR"):
                #if current word is OBTW
                if words[i] == "OBTW":
                    #if "OBTW" is start of the line, update obtw value
                    if i==0:
                        obtw = True
                    #if not, return error to main
                    else: return([False, lineCounter+1, "expected end of expression at: OBTW"])

                #if current word is TLDR
                elif words[i] == "TLDR":
                    #if no OBTW (not closed) before this TLDR, return error
                    if obtw == False: return(False, lineCounter+1, "variable does not exist: TLDR")
                    #if "TLDR" is at the end of the line, update obtw value
                    if i==len(words)-1: 
                        obtw = False
                    #if not, return error to main
                    else: return(False, lineCounter+1, "multiple line comment may not appear on the same line as code")
                
                #append token to currentLine, current word as lexeme and type is "Comment Delimiter"
                currentLine.append({"lexeme": words[i], "type": "Comment Delimiter"})
                break #to continue to the next line
            
            #skip this line, part of OBTW comment
            elif (obtw == True):
                break

            #for flagged words wth unique first word as keyword
            elif (words[i] in flaggedWords):
                for nextWord in flaggedWords[words[i]]:
                    #if next word is the next word expected for the certain flagged word, increment skip and concatenate nextWord to lexeme
                    if (i+skip+1) < len(words) and words[i+skip+1] == nextWord:
                        skip += 1
                        lexeme = lexeme + " " + nextWord
                    #not the expected next word of flagged word, reset lexeme to current word and skip's value to 0
                    else: 
                        lexeme, skip = words[i], 0

            #for flagged words with not unique first word as keyword
            elif words[i] in flaggedWords2:
                alreadyComplete = True #flag if current word is complete as a keyword
                skip = 0
                for possibleNextWords in flaggedWords2[words[i]]:
                    for nextWord in possibleNextWords:
                        #if next word is the next word expected for the certain flagged word, increment skip and concatenate nextWord to lexeme
                        if (i+skip+1) < len(words) and words[i+skip+1] == nextWord:
                            skip += 1
                            lexeme = lexeme + " " + nextWord
                        #not the expected next word of flagged word, set alreadyComplete to False, reset lexeme to current word and skip's value to 0
                        else:
                            alreadyComplete = False
                            lexeme = words[i]
                            skip = 0
                    #if alreadyComplete remained True, all expected next words was found and concatenated
                    if alreadyComplete == True:
                        break

            #create token for current lexeme
            currentToken = {}
            withMatch = False #flag if lexeme was matched to a regex
            for regex in regexPatterns:
                #if lexeme matches current regex, append lexeme and its type (in a dictionary) to currentToken, and append currentToken to currentLine, set withMatch to True
                if re.match(regex, lexeme):
                    currentToken["lexeme"] = lexeme
                    currentToken["type"] = regexPatterns[regex]
                    currentLine.append(currentToken)
                    withMatch = True
                    break
            #lexeme was not matched to any regex patterns, return error
            if withMatch == False:
                return([False, lineCounter+1, "unknown token at: " + lexeme])
        symbolTable.append(currentLine) #append currentLine to symbolTable
    return symbolTable if obtw==False else [False, 1, "Segmentation Fault"] #return lexemeList if there is no OBTW comment or was closed by a "TLDR", else return error