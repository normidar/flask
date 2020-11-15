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
import apps.engines.character as character
app.register_blueprint(character.bp,url_prefix=url_prefix+'/character')

@app.route("/")
def normal():
    return jsonify("success")

@app.before_first_request
def create_tables():
    from apps.models.models import User
    from apps.models.character import Character

    db.create_all()
    # 创建管理员角色
    rows = db.session.query(User).count()
    if rows == 0:
        admin_chara = Character(
            name='admin',
            can_edit_article = True,
            can_edit_character = True,
            can_edit_tree = True,
        )
        db.session.add(admin_chara)
        normal_chara = Character(
            name='normal',
        )
        db.session.add(normal_chara)
        # 创建超级用户
        admin_user = User(username='admin',character_id = 1)
        admin_user.hash_password('admin')
        db.session.add(admin_user)
        db.session.commit()
    