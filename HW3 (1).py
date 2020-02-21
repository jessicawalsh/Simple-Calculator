#HW 2
#Due Date: 09/21/2018, 11:59PM
########################################
#                                      
# Name: Jessica Walsh   
# Collaboration Statement: I completed this assignment alone          
#
########################################


def findNextOpr(txt):
    """
        Takes a string and returns -1 if there is no operator in txt, otherwise returns 
        the position of the leftmost operator. +, -, *, / are all the 4 operators

        >>> findNextOpr('  3*   4 - 5')
        3
        >>> findNextOpr('8   4 - 5')
        6
        >>> findNextOpr('89 4 5')
        -1
    """
    if len(txt)<=0 or not isinstance(txt,str):
        return "type error: findNextOpr"

    # --- YOU CODE STARTS HERE
    oprs='+*/-^'
    for index in range(len(txt)):
        if txt[index] in oprs:
            return index
    return -1


    # ---  CODE ENDS HERE


def isNumber(txt):
    """
        Takes a string and returns True if txt is convertible to float, False otherwise 

        >>> isNumber('1   2 3')
        False
        >>> isNumber('-  156.3')
        False
        >>> isNumber('29.99999999')
        True
        >>> isNumber('    5.9999 ')
        True
    """
    if not isinstance(txt, str):
        return "type error: isNumber"
    if len(txt)==0:
        return False

    # --- YOU CODE STARTS HERE
    try:
        float(txt)
        return True
    except:
        return False

    # ---  CODE ENDS HERE

def getNextNumber(expr, pos):
    """
        expr is a given arithmetic formula of type string
        pos is the start position in expr
          1st returned value = the next number (None if N/A)
          2nd returned value = the next operator (None if N/A)
          3rd retruned value = the next operator position (None if N/A)

        >>> getNextNumber('8  +    5    -2',0)
        (8.0, '+', 3)
        >>> getNextNumber('8  +    5    -2',4)
        (5.0, '-', 13)
        >>> getNextNumber('4.5 + 3.15         /   5',0)
        (4.5, '+', 4)
        >>> getNextNumber('4.5 + 3.15         /   5',10)
        (None, '/', 19)
    """

    if len(expr)==0 or not isinstance(expr, str) or pos<0 or pos>=len(expr) or not isinstance(pos, int):
        return None, None, "type error: getNextNumber"
    # --- YOU CODE STARTS HERE

    oprPos=findNextOpr(expr[pos:])

    if oprPos==-1:
        newOpr=None
        oprPos=None
        newNumber=expr[pos:]
    else:
        oprPos+=pos
        newOpr=expr[oprPos]
        newNumber=expr[pos:oprPos]

    if isNumber(newNumber):
        return float(newNumber), newOpr,oprPos
    else:
        return None, newOpr, oprPos


    # ---  CODE ENDS HERE

def exeOpr(num1, opr, num2):

    #This function is just an utility function for calculator(expr). It is skipping type check

    if opr=="+":
        return num1+num2
    elif opr=="-":
        return num1-num2
    elif opr=="*":
        return num1*num2
    elif opr=="/":
        return num1/num2
    elif opr=="^":
        base=int(num1)
        exponent=int(num2)
        if exponent==0:
            return 1
        elif exponent==1:
            return base
        else:
            total=base
            for i in range(exponent-1):
                total=(total*base)
            return float(total)
    else:
        return "error in exeOpr"

    
def calculator(expr):
    """
        Takes a string and returns the calculated result if the arithmethic expression is value,
        and error message otherwise 

        >>> calculator("   -4 +3 -2")
        -3.0
        >>> calculator("-4 +3 -2 / 2")
        -2.0
        >>> calculator("-4 +3   - 8 / 2")
        -5.0
        >>> calculator("   -4 +    3   - 8 / 2")
        -5.0
        >>> calculator("23 / 12 - 223 + 5.25 * 4 * 3423")
        71661.91666666667
        >>> calculator("2 - 3*4")
        -10.0
        >>> calculator("4++ 3 +2")
        'error message'
        >>> calculator("4 3 +2")
        'input error line B: calculator'
    """


    if len(expr)<=0 or not isinstance(expr,str): #Line A     
        return "input error line A: calculator"
    
    # Concatenate '0' at he beginning of the expression if it starts with a negative number to get '-' when calling getNextNumber
    # "-2.0 + 3 * 4.0 ” becomes "0-2.0 + 3 * 4.0 ”. 
    expr=expr.strip()
    if expr[0]=="-":
        expr = "0 " + expr
    newNumber, newOpr, oprPos = getNextNumber(expr, 0)   

    # Initialization. Holding two modes for operator precedence: "addition" and "multiplication"
    if newNumber is None: #Line B
        return "input error line B: calculator"
    elif newOpr is None:
        return newNumber
    elif newOpr=="+" or newOpr=="-":
        mode="add"
        addResult=newNumber     #value so far in the addition mode     
    elif newOpr=="*" or newOpr=="/":
        mode="mul"
        addResult=0
        mulResult=newNumber     #value so far in the mulplication mode
        addLastOpr = "+"
    elif newOpr=="^":
        mode="pow"
        addResult=0
        mulResult=0
        powTotal=newNumber    #value so far in the exponent mode
        powLastOpr="+"
        prevMode="add"
    pos=oprPos+1                #the new current position
    opr=newOpr                  #the new current operator
    
    #Calculation starts here, get next number-operator and perform case analysis. Conpute values using exeOpr 
    while True:
    # --- YOU CODE STARTS HERE
    
        newNumber, newOpr, oprPos=getNextNumber(expr,pos)

        if newNumber is None:
            return 'Error'

        #reset variables
        elif newOpr is None:            
            if mode=='pow':
                powTotal=exeOpr(powTotal,opr,newNumber)
                if prevMode=='mul':
                    mulResult=exeOpr(mulResult, powLastOpr, powTotal)
                    addResult=exeOpr(addResult, addLastOpr, mulResult)
                else:
                    addResult=exeOpr(addResult, powLastOpr, powTotal) 
            elif mode=='mul':
                mulResult=exeOpr(mulResult,opr,newNumber)
                addResult=exeOpr(addResult,addLastOpr,mulResult)
            else:
                addResult=exeOpr(addResult,opr,newNumber)                
            return addResult
        
        #when mode is pow and subtraction or addition is the next operator
        elif mode=='pow':
            powTotal=exeOpr(powTotal,opr,newNumber)
            if newOpr=='+' or newOpr=='-':
                mode='add'
                if prevMode=='add':
                    addResult=exeOpr(addResult,powLastOpr,powTotal)
                else:
                    mulResult=exeOpr(mulResult,powLastOpr,powTotal)
                    addResult=exeOpr(addResult,powLastOpr,mulResult)
            elif newOpr=='*' or newOpr=='/':
                mode='mul'
                if prevMode=='add':
                    mulResult=powTotal
                    addLastOpr=powLastOpr
                else:
                    mulResult=exeOpr(mulResult,powLastOpr,powTotal)
                    
        #when mode is mul and there is addition or subtraction 
        elif mode=='mul':
            if newOpr=='+' or newOpr=='-':
                mode=='add'
                mulResult=exeOpr(mulResult,opr,newNumber)
                addResult=exeOpr(addResult,addLastOpr,mulResult)
                mulResult=0
            elif newOpr=='*' or newOpr=='/':
                mulResult=exeOpr(mulResult,opr,newNumber)
            elif newOpr=='^':
                mode='pow'
                prevMode='mul'
                powTotal=newNumber
                powLastOpr=opr
                
        elif mode=='add':
            if newOpr=='+' or newOpr=='-':
                addResult=exeOpr(addResult,opr,newNumber)
            elif newOpr=='*' or newOpr=='/':
                mode='mul'
                mulResult=newNumber
                addLastOpr=opr
            elif newOpr=='^':
                mode='pow'
                prevMode='add'
                powTotal=newNumber
                powLastOpr=opr
                
        pos=oprPos+1
        opr=newOpr                        
       

    # ---  CODE ENDS HERE
