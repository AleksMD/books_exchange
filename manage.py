import os
import sys
from flask_script import Manager
from main import create_app
from flask_migrate import MigrateCommand
from tests.manager_test_command import Test

test_path = os.getcwd() + '/tests'

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    if sys.argv[1] == 'runtests':
        test = Test(test_path=test_path)
        test.run()
    else:
        manager.run()
