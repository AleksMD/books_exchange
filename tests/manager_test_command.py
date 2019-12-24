from flask_script import Command
import unittest
import os


class Test(Command):
    """
    Runs all testcases
    """

    def __init__(self, test_path=os.getcwd()):
        super().__init__()
        self.test_path = test_path

    def run(self):
        tests = unittest.TestLoader().discover(self.test_path, pattern='test*.py')
        unittest.TextTestRunner(verbosity=2).run(tests)
