import os
import unittest

from flask_script import Manager

from app import swaggerui_blueprint
from app.session import create_app



app = create_app(os.getenv('SESSION_ENV') or 'dev')
app.register_blueprint(swaggerui_blueprint)
app.app_context().push()
manager = Manager(app)

@manager.command
def run():
    app.run(host="0.0.0.0", port=8000)

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('.', pattern='test*.py')
    print(tests)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()