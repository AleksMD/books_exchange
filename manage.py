from flask_script import Manager, Server
from main import create_app
from flask_migrate import MigrateCommand
manager = Manager(create_app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
