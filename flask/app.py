from flask import Flask

app = Flask(__name__)


@app.route('/api')
def hello_world():
    return 'Hello World!'

from view.view import test
from view.main import main
from view.usr import usr
from view.background import background
from view.forum import forum

from flask_cors import *

app.register_blueprint(test, url_prefix="/api/test")
app.register_blueprint(main, url_prefix="/api/main")
app.register_blueprint(usr, url_prefix="/api/usr")
app.register_blueprint(background, url_prefix="/api/background")
app.register_blueprint(forum, url_prefix="/api/forum")

CORS(app, resources=r'/*')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
