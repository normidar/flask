from model import *

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

# 检查登录状态
@app.route('/api/v1/auth/check', methods = ['POST'])
@swag_from('doc/auth_check.yml')
def auth_check():
    verify_password(request.headers.get('token'))
    return jsonify({'data': 'Hello, %s!' % g.user.username})


# 登录
@app.route('/api/v1/auth/login', methods = ['POST'])
@swag_from('doc/auth_login.yml')
def login():
    username = request.values.get('username')
    password = request.values.get('password')
    if username is None or password is None:
        abort(400)   # missing arguments
    if verify_password(username, password):
        return get_auth_token()
    else:
        return jsonify({'失败':'fail'})

def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


# 注册
@app.route('/api/v1/auth/register', methods=['POST'])
@swag_from('doc/auth_register.yml')
def new_user():
    username = request.values.get('username')
    password = request.values.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})
