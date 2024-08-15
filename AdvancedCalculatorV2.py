# Advanced Calculator
#
# Author : Noam Paskaro
# Rules  : * Native Python only
#          * No Cast exception based input validation



IsNegNumber = lambda num : True if num[:1] == "-" and num[-1:].isnumeric() else False

ALLOWED_CHARACTERS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '+', "-", "*", "/", "^", "√", "(", ")"}
ORDER_OF_OPERATION = [('^', '√'), ('*', '/'), ('+', '-')]
OPERATORS          = "+-*/^√"


    
def FormatInput(equation):
    """ This function is used to convert a string eqation to 'tokens' """
    
    LastTokenNumerable = False
    equationTokens     = ""
    bracketCount       = 0
    lastChar           = "+"    
    
    # Remove spaces from equation
    equation = equation.replace(" ","")
    
    # TRUE if equation is empty
    if not equation:
        print("[INVALID INPUT] Empty input")
        return False
    
    # TRUE if equation contain illegale characters
    if illegalCharacters := set(equation).difference(ALLOWED_CHARACTERS):
       
       # Conditionally print the illegal character\s that were inputed
       print (f"[INVALID INPUT] {'Illegal characters were' if len(illegalCharacters) > 1 else 'An illegal character was'} enterd: {'' ', '.join(illegalCharacters)}")
       return False
    
    # Iterate over equation
    for char in equation:    
        
        match char:
            
            # char is numerable
            case str(char) if char.isnumeric() or char == ".":
                equationTokens += char
            
            # char is operator
            case "+" | "*" | "/" | "^" | "√" | "(" | ")":
                equationTokens += f" {char} "
            
            case "-":
                
                # char is operator
                if lastChar.isnumeric():
                    equationTokens += f" {char} "
                
                # char is numerable (minus)
                else:
                    equationTokens += char
        
        lastChar = char
                
    # Convert string to List
    equationTokens = equationTokens.split()
    
    # TRUE if equation contain one token
    if len(equationTokens) - equationTokens.count('(') - equationTokens.count(')') == 1:
        print("[INVALID INPUT] Not an equation")
        return False
    
    # Enumerates over the tokens and thier index
    for index, token in enumerate(equationTokens):
        
        # TRUE if the token is numerable
        if token[0].isnumeric() and token[-1:].isnumeric() or IsNegNumber(token):
              
            # TRUE if double minus
            while equationTokens[index].startswith("--"):
                equationTokens[index] = equationTokens[index][2:]
                                    
            # TRUE if back to back numerables
            if LastTokenNumerable:
                print("[INVALID INPUT] Bad equation structure")
                return False

            # TRUE if a token contains more then one "."
            if token.count(".") > 1:
                print("[INVALID INPUT] Two or more '.' in the same number")
                return False
            
            LastTokenNumerable = True
        
        # TRUE if the token is an operator
        elif len(token) == 1 and token in OPERATORS:
            
            # TRUE if back to back operators
            if not LastTokenNumerable:
                
                # TRUE if token is "√"
                if token == "√":
                    
                    try:
                        
                        # TRUE if ^√ is enterd
                        if equationTokens[index - 1] == "^":
                            print("[INVALID INPUT] Ambiguous expressions")
                            return False
                    
                    except IndexError:
                        pass
                    
                    equationTokens.insert(index, "2")
                    LastTokenNumerable = True
                
                else:
                    print("[INVALID INPUT] Bad equation structure")
                    return False
            
            else:
                LastTokenNumerable = False
            
            try:
                equationTokens[index+1]
            
            # Test if operatoe is at last index
            except IndexError:
                print("[INVALID INPUT] Equation can't end with operator")
                return False
            
            
        # TRUE if token is a bracket
        elif token == "(" or token == ")":
            
            # Running count of brackets pairs
            bracketCount += 1 if token == "(" else -1
            
            # TRUE if at a given point the number of ')' if larger then the number of '('
            if bracketCount < 0:
                print(f"[INVALID INPUT] Invalid use of closing brackets")
                return False
            
            # TRUE if empty bracket pair is entered
            # Safe because if ')' at index 0 bracketCount whould be negative and the function whould exit
            if token == ")" and equationTokens[index - 1] == "(": 
                print(f"[INVALID INPUT] Empty bracket pair")
                return False
                    
            
        # Sanity check
        else:
            print(f"[INVALID INPUT] {token} isn't a legal number or operator")
            return False
    
    # TRUE if bracketCount isn't 0, not even pairs
    if bracketCount:
        print(f"[INVALID INPUT] Unbalanced use of brackets")
        return False

    print(' '.join(equationTokens))
    return(equationTokens)



def Calculate(num1, operator, num2): 
    """ This function is used to preform a math operation on two numbers """
    
    try:
        match operator:
            
            # operator is '+'
            case "+":
                return(num1 + num2)
            
            # operator is '-'
            case "-":
                return(num1 - num2)
            
            # operator is '*'
            case "*":
                return(num1 * num2)
            
            # operator is '/'    
            case "/":
                try:
                    return(num1 / num2)
                
                # Test for zero division error      
                except ZeroDivisionError:
                    print("[ILEGAL OPERATION] Dividing by zero")
                    
                    # Abort and restart
                    main()
                    
            # operator is '^'
            case "^":
                return(num1 ** num2)
            
            # operator is '√'
            case "√":
                return(num2 ** (1 / num1))
    
    except OverflowError:
        print("[ILEGAL OPERATION] Calculation result too long")
                    
        # Abort and restart
        main()


def FindIndex (equation, operation):
    """ This function is used to return the index of the first occurrence of
    either of two elements in a list """
    
    # Could be done using a simple enumerate loop but this is cooler
    
    try:
        index = equation.index(operation[0])
    
    # operation[0] wasn't found in list
    except ValueError:
        try:
            index = equation.index(operation[1])
            return index   # Only operation[1] found

        # operation[1] wasn't found in list
        except ValueError:
            return False   # Neither operations were found
    
    # operation[0] found in list
    else:
        try:
            
            # TRUE if operation[0] was found before operation[1]
            if equation.index(operation[1]) < index:
                index = equation.index(operation[1])
            return index   # Both operations were found
        
        # operation[1] wasn't found in list
        except ValueError:
            return index   # Only operation[0] found



def FindIndexB (equation, operation, reverse):
    
    for index, token in enumerate(equation[::-1 if reverse else 1]):
        print(token)
        if token == operation[0] or token == operation[1]:
            return len(equation) - index - 1 if reverse else index 
    
    return False



def BracketFind(equation):
    """ This function is used to find the index of the next bracket pair"""
    
    # Iterate over equaation tokens
    for index, token in enumerate(equation):
        
        # TRUE if '(' found
        if token == "(":
            
            # Store the index of the last '(' found
            lastOpenIndex = index
        
        # TRUE if ')' found
        if token == ")":
            return (lastOpenIndex, index)
    
    return False, False



def Solve(equation, operation):
    """ This function is used to break the eqution into simple caculations """

    # TRUE if the operations were found in the equation
    if index := FindIndex(equation, operation):
        
        # Calls the Calculate funtion on the individual calculation
        result = (Calculate(float(equation[index-1]), equation[index], float(equation[index+1])))
        print(f"{equation[index-1]} {equation[index]} {equation[index+1]} = {result}")
        
        # Insert the calculation result into the equation
        equation[index-1] = result
        
        # Remove the "used" tokens
        equation.pop(index)
        equation.pop(index)
        
        # Recursivly call this function on the new equation
        Solve(equation, operation)
    
    return equation



def Simplfy(equation):
    """ This function is used to simplify the function before it solved """
    
    index = 0

    # Used to iterate over equation 
    while index < len(equation): # Not using for because equation is being tampered with
        match equation[index]:
            
            # equation[index] is '-'
            case "-":
                
                # TRUE if the last token is a negative number
                if IsNegNumber(equation[index + 1]):
                    
                    # Replace current token with '+'
                    equation[index] = '+'
                    
                    # Remove the negative sign from the next token
                    equation[index + 1] = equation[index + 1][1:]
                    
                    simpFlag = True
                    
            # equation[index] is '√'
            case "√":
                try:
                    
                    # TRUE if thier is another root operation before this one
                    if equation[index - 2] == "√":
                        
                        # Calculates the new root level? (idk the tiny number abuove the sign)
                        equation[index - 3] = str(int(equation[index - 1]) * int(equation[index - 3]))
                        
                        # Remove optimized tokens
                        equation.pop(index - 1)
                        equation.pop(index - 1)
                        
                        # Move the index back to places to compensate for the token removal
                        index -= 2
                        
                        simpFlag = True
                        
                except IndexError:
                    pass

        index += 1
        
    return equation



def main():

    # Continuous loop
    while True:
        
        # TRUE if FormatInput return value isn't False
        if equation := FormatInput(input("Enter you equation: ")):
            
            # Save unmodified version for final print
            originalEqua = equation.copy()
            
            Simplfy(equation)
            
            # TRUE if equation was simplified
            if not equation == originalEqua:
                print(''.join(equation))
                pass
            
            # Iterate while thier are "(" in the equation
            while equation.count("("):
                startIndex, endIndex = BracketFind(equation)
                
                # Remove the bracket
                equation.pop(startIndex)
                equation.pop(endIndex - 1)
                                
                # Iterate over operation in order
                for operation in ORDER_OF_OPERATION:
                    
                     # Pass the "in bracket" part to Solve
                    equation[startIndex:endIndex - 1] = Solve(equation[startIndex:endIndex - 1], operation)
                            
            # Iterate over operation in order
            for operation in ORDER_OF_OPERATION:
                Solve(equation, operation)
                   
            print(f"{' '.join(originalEqua)} = {equation[0]}")
    
if __name__ == "__main__":
    main()