from flask import Blueprint, jsonify, request, abort, g,url_for
from flasgger import swag_from

from apps import db
from apps.models.models import User
from apps.models.character import Character

bp = Blueprint('auth', __name__)
doc_path = '../doc/auth'

# 验证控制权
def check_ability():
    if verify_password(request.headers.get('token')):
        chara_id = g.user.character_id
        chara = Character.query.filter_by(id=chara_id).one()
        if chara_id==1:
            return True
        elif chara_id == 2:
            return False
        elif chara.check_can('can_edit_auth'):
            return True
    return False

# @auth.verify_password
def verify_password(username_or_token, password = ""):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

# 更改用户信息
def user_update():
    id = request.values.get('id')
    chara_id = request.values.get('chara_id')
    if check_ability() and id is not None and chara_id is not None:
        User.query.filter_by(id=id).update({'character_id':chara_id})
        return jsonify({'message':'success'})
    else:
        return '权限不足',403


# 登录
@bp.route('/login', methods = ['POST'])
@swag_from(doc_path + '/auth_login.yml')
def login():
    username = request.values.get('username')
    password = request.values.get('password')
    if username is None or password is None:
        return "传值不正确",422
    if verify_password(username, password):
        return get_auth_token()
    else:
        return '用户名或密码错误',400
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'message': 'success'})


# 注册
@bp.route('/register', methods=['POST'])
@swag_from(doc_path + '/auth_register.yml')
def new_user():
    username = request.values.get('username')
    password = request.values.get('password')
    if username is None or password is None:
        return '参数不足',422
    if User.query.filter_by(username=username).first() is not None:
        return '用户名已经被注册',423
    user = User(username=username,character_id = 2)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': user.username})

#是否已注册
@bp.route('/check', methods=['GET'])
@swag_from(doc_path + '/auth_check.yml')
def check_user():
    username = request.values.get('username')
    if User.query.filter_by(username=username).first() is not None:
        return "200"
    return "找不到用户名",404


# 测试接口
@bp.route('/test', methods=['POST'])
def test():
    return jsonify(request.values.dicts)