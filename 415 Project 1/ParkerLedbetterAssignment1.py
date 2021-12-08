
#==========================================================================
## I CERTIFY THAT THE CODE SHOWN BELOW IS MY OWN WORK
## AND THAT I HAVE NOT VIOLATED THE UNCW ACADEMIC HONOR CODE
## WHILE WRITING THIS CODE
## no additional import statements please
## If the function is not complete as instructed, you get
## AT BEST 50% of the grade for that question.

# PROGRAM PURPOSE:... Python Basic Skills
# AUTHOR:............ Ledbetter, Parker
# COURSE:............ CSC 415-515
# TERM:.............. Fall 2020
# COLLABORATION:..... None
#==========================================================================
from typing import List, Any

from testing import test
import sys
import random

#==========================================================================
# q1 - create function letterGrade() to meet the conditions below
#    - accept 1 integer parameter between 0-100
#    - add a meaningful docstring
#    - letterGrade(x) accepts one integer and determines what the corresponding
#    - letter grade is (A: >=90; B: 80-89; C: 70-79; D: 60-69; F: <60).
#    --- e.g. submitted int is 91; return value is A
#    --- e.g. submitted int is 89; return value is B
#    --- e.g. submitted int is 70; return value is C
#    --- e.g. submitted int is 52; return value is F
#    - Returns letter grade as string
#==========================================================================
def letterGrade(grade):
    """This function takes in an integer value grade and returns the letter grade associated"""
    value = int(grade)
    if value >= 90:
        return "A"
    if value >= 80 and value <= 89:
        return "B"
    if value >= 70 and value <= 79:
        return "C"
    if value >= 60 and value <= 69:
        return "D"
    else:
        return "F"
    

#==========================================================================
# q2 - create function isIntDiffEven() to meet the conditions below
#    - accept 2 integer parameters of any value
#    - add a meaningful docstring
#    - determine if the integer difference between the values is even.
#    --- e.g. submitted ints are -7 and 12; diff is -19(odd); returns False
#    --- e.g. submitted ints are 13 and 9; diff is 4(even); returns True
#    --- e.g. submitted ints are -2 and -5; diff is 3(odd); return False
#    --- you may assume the user arguments will be integers
#    - return the result
#==========================================================================
def isIntDiffEven(first,second):
    """This function takes two int values and determines if the difference between the two is even."""
    first_value = int(first)
    second_value = int(second)
    difference_value = first_value - second_value
    if difference_value % 2 == 0:
        return True
    else:
        return False


#==========================================================================
# q3 - create function hasSameNumElements() to meet the conditions below
#    - add a meaningful docstring
#    - accept 2 parameters which are type sequence (tuple, list or string)
#    - return True if user args have the same # of elements; False otherwise
#    --- args ('h','i') and [1,2,3]; function returns False
#    --- args [1776,1789] and ('hello','Jo'); function returns True
#    --- args 'boo' and [10, 'four', 2.575]; function returns True
#    - you are not allowed to use len function.
#    - return the result
#==========================================================================
def hasSameNumElements(first, second):
    """This function returns True if two arguments have the same number of elements."""
    first_counter = 0
    second_counter = 0
    for i in first:
        first_counter += 1
    for i in second:
        second_counter += 1
    if first_counter == second_counter:
        return True
    else:
        return False


        
#==========================================================================
# q4 - create function getUserCharInput() to meet the conditions below
#    - add a meaningful docstring
#    - accept 5 parameters which are type string (alphabet letters)
#    - prompt user to input a letter
#    - if the input does not meet conditions, prompt for input until it does
#    - accept the input if it is same as any the five letters
#    --- e.g. params: A, r, e, G, t, prompt for input until user enters
#    --- any of those five letters
#    --- userinputs:
#    - i
#    - k
#    - e -> valid input; return e
#    - return the valid userinput
#==========================================================================
def getUserCharInput(first, second, third, fourth, fifth):
    """This function accepts str input from a user and prompts them until they enter the given 5 letters. Returns valid input."""
    validChar = [first, second, third, fourth, fifth]
    userInput = str(input('Please enter a valid character: '))
    for i in validChar:
        if i == userInput:
            return userInput
        else:
            userInput = str(input('Sorry, Please enter a valid character: '))


#==========================================================================
# q5 - create function backward() to meet the conditions below
#    - accept one string parameter of any value
#    - add a meaningful docstring
#    - returns the backward string,
#    --- e.g. submitted value is diaper; result repaid
#    --- e.g. submitted value is desserts; result stressed
#    --- e.g. submitted value is god; result dog
#    - return the result
#==========================================================================
def backward(word):
    """This function will return a string backwards."""
    return word[::-1]


#==========================================================================
# q6 - create function print2DListContent() to meet the conditions below
#    - accepts a list: the list is a 2-D list of arbitrary content
#    - add a meaningful docstring
#    - prints each stored value on a different line.
#    - example:
#    --- list2D = [['red','square','one'], ['yellow','triangle'], ['circle', 'blue']]
#    --- displays:
    # red
    # square
    # one
    # yellow
    # triangle
    # circle
    # blue
#    - return: None
#==========================================================================
def print2DListContent(list):
    """This function is passed a 2D-list and prints each element a line at a time."""
    for i in list:
        for k in i:
            print(k)

            

#==========================================================================
# q7 - create function createPlates() to meet the conditions below
#    - Accepts a list of 3-letter strings, and a list of 4-digit strings
#    - add a docstring
#    - returns a new list representing all possible combinations of EACH
#    - 3-letter string and EACH 4-digit numbers with a dash ('-') in between
#    --- Example 1: create_plates(["ZQQ", "AEE"], [1234, 4567])
#    --- returns the list ["ZQQ-1234","ZQQ-4567","AEE-1234","AEE-4567"]
#    --- Example 2: create_plates(["ZQQ", "BRP", "AEE"], [1234, 4567])
#    --- final list:
#    --- ["ZQQ-1234","ZQQ-4567","BRP-1234", "BRP-4567","AEE-1234","AEE-4567"]
#    - return the result
#==========================================================================
def createPlates(strList, digList):
    """This function returns a list of all possible combinations of a license plate. Ex: ZQQ-1234"""
    output = []
    plate = ''
    for i in strList:
        for k in digList:
            plate = (str(i)+'-'+str(k))
            output.append(plate)
    return output



#==========================================================================
# q8 - create function my_max() to meet the conditions below
#    - accept 2 numeric parameters
#    - add a docstring
#    - determine the greater of a and b
#    --- e.g. submitted values are 8 and -3.5; max is 8
#    --- e.g. submitted values are -5 and -3; max is -3
#    --- e.g. submitted values are 15 and 150; max is 150
#    --- You are not allowed to use built in max or min functions!
#    - return the maximum of a and b
#==========================================================================
def my_max(x, y):
    """This function returns the larger value given."""
    if x > y:
        return x
    else:
        return y




#==========================================================================
# q9 - create function positiveIntDiff() to meet the conditions below
#    - accept 2 integer parameters of any value
#    - add a docstring
#    - determine the positive integer difference between the values
#    --- e.g. submitted ints are -7 and 12; +diff is 19
#    --- e.g. submitted ints are 13 and 9; +diff is 4
#    --- e.g. submitted ints are -2 and -5; +diff is 3
#    --- you may assume the user arguments will be integers
#    --- You are not allowed to use built in abs function!
#    - return the result
#==========================================================================
def positiveIntDiff(first, second):
    """This function returns the integer difference between 2 values."""
    first = int(first)
    second = int(second)
    if first > second:
        diff = first - second
        return diff
    if second > first:
        diff = second - first
        return diff


#==========================================================================
# q10 - create function sumPos() to meet the conditions below
#    - accept a list of numeric values
#    - add a docstring
#    - calculate the sum of the positive values
#    --- e.g. submitted list is [2,9,-5,1]; sum is 12
#    --- e.g. submitted list is [-1,-2,-5]; sum is 0
#    --- e.g. submitted list is [1.5,-4,2.5]; sum is 4
#    --- You are not allowed to use built in sum function!
#    - return the sum
#==========================================================================
def sumPos(list):
    """This function returns a sum of positive values from a given list."""
    counter = 0
    for i in list:
        if list[i] > 0:
            counter += list[i]
    return counter


#==========================================================================
# *************************************************************************
# ******************* DO NOT EDIT CODE BELOW THIS POINT *******************
# *************************************************************************
#==========================================================================
def printErr():
    print(" ",sys.exc_info()[0].__name__,"-line",sys.exc_info()[-1].tb_lineno)
    print(" ",sys.exc_info()[1])

def test_letterGrade():
    results = []
    print("\n\t\t**** (10 points) - letterGrade() ****")
    num = random.randint(90,100)
    results.append(test('A', letterGrade, num))    
    results.append(test('A', letterGrade, 90))
    
    num = random.randint(80,89)
    results.append(test('B', letterGrade, num))
    
    num = random.randint(70,79)
    results.append(test('C', letterGrade, num))
    
    num = random.randint(60,69)
    results.append(test('D', letterGrade, num))
    results.append(test('D', letterGrade, 60))

    num = random.randint(0,59)
    results.append(test('F', letterGrade, num))

    if False in results and True not in results:
        print('\nFailed all the tests')
    elif False in results:
        print('\nFailed some of the tests.')
    else:
        print('\nPassed all the tests.')
   
def test_isIntDiffEven():
    results = []
    print("\n\t\t**** (10 points) - isIntDiffEven() ****")
    for i in range(3):        
        a = random.randint(-30,5)
        b = random.randint(-5,30)
        results.append(test(not((a-b)%2), isIntDiffEven, a, b))        
        results.append(test(not((max(a,b)-min(a,b))%2), isIntDiffEven, b, a))
        
    if False in results and True not in results:
        print('\nFailed all the tests')
    elif False in results:
        print('\nFailed some of the tests.')
    else:
        print('\nPassed all the tests.')

def test_hasSameNumElements():
    results = []
    print("\n\t\t**** (10 points) - hasSameNumElements() ****")
    lst = ['Tom', ('orange', 'apple', 'banana'), ['orange', 'apple', 'banana', 'cherry'],
           'book', [1, 2], [1, 2, 3], (5, 6, 7, 8)]
    for i in range(3):        
        a = random.randint(0,6)
        b = random.randint(0,6)
        results.append(test(len(lst[a])==len(lst[b]), hasSameNumElements, lst[a], lst[b]))
    results.append(test(True, hasSameNumElements, lst[a], lst[a]))
            
    if False in results and True not in results:
        print('\nFailed all the tests')
    elif False in results:
        print('\nFailed some of the tests.')
    else:
        print('\nPassed all the tests.')

def test_getUserCharInput():
    import string
    results = []
    print("\n\t\t**** (10 points) - getUserCharInput() ****")
    alpha = string.ascii_letters
    for i in range(3):
        a = random.choice(alpha)
        b = random.choice(alpha)
        c = random.choice(alpha)
        d = random.choice(alpha)
        e = random.choice(alpha)
        print('\nArguments passed to the functions are {}, {}, {}, {}, and {}'.format(a, b, c, d, e))
        ui = getUserCharInput(a, b, c, d, e)
        if ui in a+b+c+d+e:            
            results.append(True)
        else:          
            results.append(False)
            
    if False in results and True not in results:
        print('\nFailed all the tests')
    elif False in results:
        print('\nFailed some of the tests.')
    else:
        print('\nPassed all the tests.')    

def test_backward():
    results = []
    print("\n\t\t**** (10 points) - backward() ****")
    smd = ('yensid', 'harpo', 'nacirema', 'erewhon', 'yob', 'silopanna', 
        'retsof', 'llareggub', 'dog', 'diaper', 'repaid', 'desserts',
        'disney', 'oprah', 'american', 'nohwere', 'boy', 'annapolis', 
        'foster', 'buggerall', 'god', 'repaid', 'diaper', 'stressed')
    
    
    for i in range(5):        
        idx = random.randint(0,11)
        if idx < 12:
            results.append(test(smd[idx+12], backward, smd[idx]))
        else:
            results.append(test(smd[idx-12], backward, smd[idx]))
                           
    if False in results and True not in results:
        print('\nFailed all the tests')
    elif False in results:
        print('\nFailed some of the tests.')
    else:
        print('\nPassed all the tests.')

def test_print2DListContent():
    print("\n\t\t**** (10 points) - print2DListContent() ****")
    print('Instructor will check the output in read-time')
    print2DListContent( [['red','square', 'one'], ['yellow','triangle'], ['blue','circle', 'three']] )
    print()
    print2DListContent( [[1,2], [3,4]] )
    print()
    print2DListContent( [[3.0, 'dogs', 2], [1, 2], ['cat', 'bird', 'banana']] )

def test_createPlates():
    results = []
    print("\n\t\t**** (10 points) - createPlates() ****")
    Lo3L = ['TEK', 'EHU', 'OPB', 'THU', 'OXW']
    Lo4D = [5789, 2246, 2074, 8974, 3530, 7356]
    VLo7LD = ['EHU-2074', 'EHU-2246', 'EHU-3530', 'EHU-5789', 'EHU-7356', 'EHU-8974',
              'OPB-2074', 'OPB-2246', 'OPB-3530', 'OPB-5789', 'OPB-7356', 'OPB-8974',
              'OXW-2074', 'OXW-2246', 'OXW-3530', 'OXW-5789', 'OXW-7356', 'OXW-8974',
              'TEK-2074', 'TEK-2246', 'TEK-3530', 'TEK-5789', 'TEK-7356', 'TEK-8974',
              'THU-2074', 'THU-2246', 'THU-3530', 'THU-5789', 'THU-7356', 'THU-8974']

    Lo3L_B = ['XSH', 'VBO', 'SAJ', 'XED', 'UMA', 'ZOY', 'ZIA', 'LKW']
    Lo4D_B = [5992, 5497, 2954, 9971, 9562]
    VLo7LD_B = ['LKW-2954', 'LKW-5497', 'LKW-5992', 'LKW-9562', 'LKW-9971',
              'SAJ-2954', 'SAJ-5497', 'SAJ-5992', 'SAJ-9562', 'SAJ-9971',
              'UMA-2954', 'UMA-5497', 'UMA-5992', 'UMA-9562', 'UMA-9971',
              'VBO-2954', 'VBO-5497', 'VBO-5992', 'VBO-9562', 'VBO-9971',
              'XED-2954', 'XED-5497', 'XED-5992', 'XED-9562', 'XED-9971',
              'XSH-2954', 'XSH-5497', 'XSH-5992', 'XSH-9562', 'XSH-9971',
              'ZIA-2954', 'ZIA-5497', 'ZIA-5992', 'ZIA-9562', 'ZIA-9971',
              'ZOY-2954', 'ZOY-5497', 'ZOY-5992', 'ZOY-9562', 'ZOY-9971']
    returnedList = createPlates(Lo3L,Lo4D)
    results.append(test(returnedList, createPlates, Lo3L, Lo4D))
    returnedList = createPlates(Lo3L_B,Lo4D_B)
    results.append(test(returnedList, createPlates, Lo3L_B, Lo4D_B))
    
    if False in results and True not in results:
        print('\nFailed all the tests')
    elif False in results:
        print('\nFailed some of the tests.')
    else:
        print('\nPassed all the tests.')
        


def test_my_max():
    results = []
    print("\n\t\t**** (10 points) - my_max ****")
    for i in range(5):        
        a = random.randint(-5,1)
        b = random.randint(-1,5)
        c = max(a,b)
        results.append(test(c, my_max, a, b))

    if False in results and True not in results:
        print('\nFailed all the tests')
    elif False in results:
        print('\nFailed some of the tests.')
    else:
        print('\nPassed all the tests.')
    
def test_positiveIntDiff():
    results = []
    print("\n\t\t**** (10 points) - positiveIntDiff() ****")
    for i in range(5):        
        a = random.randint(-10,10)
        b = random.randint(9,30)
        results.append(test(max(a,b)-min(a,b), positiveIntDiff, a, b))

    if False in results and True not in results:
        print('\nFailed all the tests')
    elif False in results:
        print('\nFailed some of the tests.')
    else:
        print('\nPassed all the tests.')


def test_sumPos():
    results = []
    print("\n\t\t**** (10 points) - sumPos() ****")
    for i in range(5):        
        a = random.randint(-7,-2)
        b = random.randint(0,6)
        results.append(test(sum(list(range(0, b))), sumPos, list(range(a, b))))
    if False in results and True not in results:
        print('\nFailed all the tests')
    elif False in results:
        print('\nFailed some of the tests.')
    else:
        print('\nPassed all the tests.')

 
        
def main():

    try:
        test_letterGrade()
    except:
        print("**Something is wrong with letterGrade()")
        printErr()

    try:
        test_isIntDiffEven()
    except:
        print("**Something is wrong with isIntDiffEven()")
        printErr()

    try:
        test_hasSameNumElements()
    except:
        print("**Something is wrong with hasSameNumElements()")
        printErr()

    try:
        test_getUserCharInput()
    except:
        print("**Something is wrong with getUserCharInput()")
        printErr()        

    try:
        test_backward()
    except:
        print("**Something is wrong with backward()")
        printErr()

    try:
        test_print2DListContent()
    except:
        print("**Something is wrong with print2DListContent()")
        printErr()
        
    try:
        test_createPlates()
    except:
        print("**Something is wrong with createPlates()")
        printErr()
    try:
        test_my_max()
    except:
        print("**Something is wrong with my_max()")
        printErr()
    
    try:
        test_positiveIntDiff()
    except:
        print("**Something is wrong with positiveIntDiff()")
        printErr()

    try:
        test_sumPos()
    except:
        print("**Something is wrong with sumPos()")
        printErr()
        

main()


