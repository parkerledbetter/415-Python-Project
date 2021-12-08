#module testing
import sys, traceback

def test(expected_result, function, *params):
    """this function supports unit testing of functions. The named function is called
        with the specified parameters, and the returned result is compared to the
        expected result. The function prints details about the function call, including
        the function name and parameter values, and 
        whether the function passed or failed the test. In the event of error,
        the stack trace is printed.

        Parameters:
            expected_result: The result expected from a correct implementation
            function: The name of the function being tested
            *params: a comma-separated list of parameters to the function

        Returns:
            Nothing
    """
    
    funcName = str(function).split()[1]
    p = ""
    for x in params:
        p += str(x)+","
    p = p[:len(p)-1]
    print("Testing "+funcName+"("+str(p)+")")
    try:
        actual_result = function(*params)
        #print("\tActual result = ", actual_result, ", Expected result = ", expected_result)
        if are_equal(actual_result, expected_result):
            return True
        else:
            return False
    except:
        print(funcName + " has errors")
        traceback.print_exc()        

def are_equal(arg1, arg2):
    if type(arg1) == list:
        return have_same_values(arg1, arg2)
    else:
        return arg1 == arg2

def have_same_values(list1, list2):
    list1.sort()
    list2.sort()
    return list1 == list2
