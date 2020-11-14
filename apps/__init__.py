from flask import Flask, jsonify
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
swagger = Swagger(app)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

url_prefix = '/api/v1'
import apps.engines.auth as auth
app.register_blueprint(auth.bp,url_prefix=url_prefix+'/auth')
import apps.engines.article as article
app.register_blueprint(article.bp,url_prefix=url_prefix+'/article')
import apps.engines.tree as tree
app.register_blueprint(tree.bp,url_prefix=url_prefix+'/tree')

@app.route("/")
def normal():
    return jsonify("success")

@app.before_first_request
def create_tables():
    db.create_all()