import re

#Concatenate elements in tempSplit into one element if part of a string literal
def concatenateStringLiteral(tempSplit):
    openDQ = False
    tempList = []

    for element in tempSplit:
        #current element is opening double quote (start of string literal)
        if element == '"' and openDQ == False:
            openDQ = True                 #update openQ
            string = element              #set string's value as element

        #current element is closing double quote (end of string literal)
        elif element == '"' and openDQ == True:
            openDQ = False                #update openQ
            string += element             #concatenate string and current element
            tempList.append(string)       #append complete string literal to tempList

        #current element is part of the string
        elif openDQ == True:
            string += element            #concatenate string and current element

        #append current element to tempList since it is not part of a string
        else: tempList.append(element)
    
    #if openDQ is True, lexical error occured return list with error information
    #else, return tempList
    return [False, "unknown token at " + string] if openDQ == True else tempList
        
#Turn string to a 2D list of lexemes
def toLexeme(code):
    #keywords of more than one word (unique first word)
    flaggedWords = {"I": ["HAS", "A"], "SUM": ["OF"], "DIFF": ["OF"], "PRODUCT": ["OF"], "QUOSHUNT": ["OF"], "MOD": ["OF"], "BIGGR": ["OF"], "SMALLR": ["OF"], "EITHER": ["OF"], "WON": ["OF"], "ANY": ["OF"], "ALL": ["OF"], "IS": ["NOW", "A"], "O": ["RLY"], "YA": ["RLY"], "NO": ["WAI"]}
    #keywords of more than one word (nonunique first word)
    flaggedWords2 = {"BOTH": [["OF"], ["SAEM"]], "IM": [["IN", "YR"], ["OUTTA", "YR"]]}

    lexemeList = []
    lineCounter = 0
    obtw = False        #obtw comment flag

    #split code with new line as delimiter
    lines = code.splitlines()

    #get the lexemes per line
    for line in lines:
        lineCounter += 1

        #keep the delimiter when using re.split() : https://stackoverflow.com/questions/2136556/in-python-how-do-i-split-a-string-and-keep-the-separators
        #split line by double quotes as delimiter but keep delimiter
        tempSplit = re.split(r'(["])', line)

        #current line may have a string literal
        if '"' in tempSplit:
            tempList = concatenateStringLiteral(tempSplit) #concatenates string literal elements to one string
            if tempList[0] == True: return([False, lineCounter, tempList[1]]) #if error occured, return error to main
        #current line does not have a string literal
        else:
            tempList = [line]
        
        words = []
        for i in range (0, len(tempList)):
            #current element is a string literal, append to words as it is
            if re.match(r'["].*["]', tempList[i]):
                words.append(tempList[i])
            #concatenate words and string split result
            else:
                words += tempList[i].split()
                
        skip, currentLine = 0, []

        for i in range (0, len(words)):
            lexeme = words[i]
            #skip words because word is already concatenated to some prev word
            if skip > 0: 
                skip -= 1
                continue
            
            #ignore comments, return errors if found
            if words[i] == "BTW":
                break
            elif words[i] == "OBTW":
                #if "OBTW" is start of the line, update obtw value
                if i==0:
                    obtw = True
                    break
                #if not, return error to main
                else: return([False, lineCounter, "expected end of expression at: OBTW"])
            elif words[i] == "TLDR":
                #if no OBTW (not closed) before this TLDR, return error
                if obtw == False: return(False, lineCounter, "variable does not exist: TLDR")
                #if "TLDR" is at the end of the line, update obtw value
                if i==len(words)-1: 
                    obtw = False
                    break
                #if not, return error to main
                else: return(False, lineCounter, "multiple line comment may not appear on the same line as code")
            elif obtw == True: #current line is part of OBTW comment
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
                for possibleNextWords in flaggedWords2[words[i]]:
                    skip = 0
                    for nextWord in possibleNextWords:
                        if (i+skip+1) < len(words) and words[i+skip+1] == nextWord:
                            skip += 1
                            lexeme = lexeme + " " + nextWord
                        else:
                            lexeme = words[i]
                            skip = 0
            currentLine.append(lexeme) #append lexeme
        lexemeList.append(currentLine) if currentLine!=[] else lexemeList #append if not empty list
    return lexemeList if obtw==False else [False, 1, "Segmentation Fault"] #return lexemeList if there is no OBTW comment or was closed by a "TLDR", else return error
 
    
def checkRegex(lexemeList):
    #regex with their respective type
    regexPatterns = {"^-?(\d*\.\d+)$":"Float Literal", "^-?\d+$":"Integer Literal", "^\".*\"$": "String Literal", "^(WIN|FAIL)$":"Boolean Literal", "^(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)$":"Type Literal", "^HAI$":"Code Delimiter", "^KTHXBYE$":"Code Delimiter", "^(I[^\S\r\n]HAS[^\S\r\n]A)$": "Variable Declaration", "^ITZ$":"Variable Assignment", "^R$":"Assignment Keyword", "^(SUM[^\S\r\n]OF)$":"Arithmetic Operator", "^(DIFF[^\S\r\n]OF)$":"Arithmetic Operator", "^(PRODUKT[^\S\r\n]OF)$":"Arithmetic Operator", "^(QUOSHUNT[^\S\r\n]OF)$":"Arithmetic Operator", "^(MOD[^\S\r\n]OF)$":"Arithmetic Operator", "^(BIGGR[^\S\r\n]OF)$":"Arithmetic Operator", "^(SMALLR[^\S\r\n]OF)$":"Arithmetic Operator", "^(BOTH[^\S\r\n]OF)$":"Boolean Operator", "^(EITHER[^\S\r\n]OF)$":"Boolean Operator", "^(WON[^\S\r\n]OF)$":"Boolean Operator", "^NOT$":"Boolean Operator", "^(ANY[^\S\r\n]OF)$":"Boolean Operator", "^(ALL[^\S\r\n]OF)$":"Boolean Operator", "^(BOTH[^\S\r\n]SAEM)$":"Comparison Operator", "^DIFFRINT$":"Comparison Operator", "^SMOOSH$":"Concatenate Operator", "^MAEK$":"Typecast Operator", "^A$":"Separator", "^(IS[^\S\r\n]NOW[^\S\r\n]A)$":"Recast Operator", "^VISIBLE$":"Output Keyword", "^GIMMEH$":"Input Keyword", "^O[^\S\r\n]RLY\?$":"If Else Start", "^(YA[^\S\r\n]RLY)$":"If Keyword", "^MEBBE$":"Else If Keyword", "^(NO[^\S\r\n]WAI)$":"Else Keyword", "^OIC$":"Conditional Statement End", "^WTF\?$":"Switch Case Start", "^OMG$":"Case Keyword", "^OMGWTF$":"Default Case Keyword", "^(IM[^\S\r\n]IN[^\S\r\n]YR)$":"Loop Start", "^UPPIN$":"Loop Increment Keyword", "^NERFIN$":"Loop Decrement Keyword", "^YR$":"Separator", "^TIL$":"For Keyword", "^WILE$":"While Keyword", "^(IM[^\S\r\n]OUTTA[^\S\r\n]YR)$":"Loop End", "AN":"And Keyword", "^[a-zA-Z]\w*$":"Identifier"}

    symbolTable = []

    #access every line
    for lineCount in range (len(lexemeList)):
        currentLine = []
        #access every lexeme in current line
        for lexeme in lexemeList[lineCount]:
            currentToken = {}
            #access every regex in regexPatterns
            withMatch = False
            for regex in regexPatterns:
                #if lexeme matches current regex, append lexeme and its type (in a dictionary) to currentLexeme, and append currentLexeme to currentLine
                if re.match(regex, lexeme):
                    currentToken["lexeme"] = lexeme
                    currentToken["type"] = regexPatterns[regex]
                    currentLine.append(currentToken)
                    withMatch = True
                    break
            #if regex was not matched, unknown token error
            if withMatch == False:
                return([False, lineCount+1, "unknown token at:" + lexeme])
        symbolTable.append(currentLine) #append currentLine to symbolTable
    return symbolTable

def lexer(code):
    #get the lexemes of code string
    lexemeResult = toLexeme(code)

    #if error was encountered, return error
    if len(lexemeResult)!=0 and lexemeResult[0] == False:
        return lexemeResult
    #no error encountered
    else:
        #create a symbol table for lexeme with their type then return the symbol table
        symbolTable = checkRegex(lexemeResult)
        return symbolTable
