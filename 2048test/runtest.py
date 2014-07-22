"""
Test suite for format function in "merge in 2048"
"""

import user34_dtcu5tY7eO_0 as poc_simpletest

def run_test(format_function):
    """
    Some informal testing code
    """
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    # test format_function on various inputs
    suite.run_test(format_function([1,1,1,1,1,1]), [2,2,2,0,0,0], "Test #1:")
    suite.run_test(format_function([1,0,0,1,0,1,1,1,1,1]), [2,2,2,1,0,0,0,0,0,0], "Test #2:")
    suite.run_test(format_function([2,2]), [4,0], "Test #3:")
    suite.run_test(format_function([2]), [2], "Test #4:")
    suite.run_test(format_function([1,2,3,4]), [1,2,3,4], "Test #5:")
    
    suite.report_results()
    