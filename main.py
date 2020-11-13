from flasgger import Swagger,swag_from
from model import *

swagger = Swagger(app)

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

# 创建文章
@app.route('/api/v1/article/create', methods=['POST'])
@swag_from('doc/article_create.yml')
def article_create():
    title = request.values.get('title')
    content = request.values.get('content')
    link_id = request.values.get('link_id')
    # 登录了才可以录入
    if verify_password(request.headers.get('token')):
        owner = g.user.id
        article = Article(title=title, content=content, owner=owner, link_id=link_id)
        db.session.add(article)
        db.session.commit()
        return jsonify({'success':"success"})
    else:
        return jsonify({'fail':'fail'})

# 删除文章 创建post 修改put 删除delete 获取get
@app.route('/api/v1/article/delete', methods= ['DELETE'])
@swag_from('doc/article_delete.yml')
def article_delete():
    id = request.values.get('id')
    if verify_password(request.headers.get('token')):
        article = Article.query.filter_by(id=id).first()
        if article.owner == g.user.id:
            Article.query.filter_by(id=id).delete()
            db.session.commit()
            return jsonify({'success': '成功删除'})
        else:
            return jsonify({'fail':'只能删除自己的'})
    else:
        return jsonify({'fail':'请先登录'})

# 修改文章
@app.route('/api/v1/article/update', methods=['PUT'])
@swag_from('doc/article_update.yml')
def article_update():
    id = request.values.get('id')
    title = request.values.get('title')
    content = request.values.get('content')
    link_id = request.values.get('link_id')
    # 登录了才可以录入
    if verify_password(request.headers.get('token')):
        insert_map = {}
        if title != "": insert_map['title'] = title
        if content != "": insert_map['content'] = content
        if link_id != "": insert_map['link_id'] = link_id
        # 
        article = Article.query.filter_by(id=id).first()
        if article.owner == g.user.id:
            Article.query.filter_by(id=id).update(insert_map)
            db.session.commit()
            return jsonify({'success': '成功更改'})
        else:
            return jsonify({'fail':'只能更改自己的'})
    else:
        return jsonify({'fail':'请先登录'})

# 获取文章列表
@app.route('/api/v1/article/view', methods = ['POST'])
def article_view():
    if verify_password(request.headers.get('token')):
        userid = g.user.id
        all_articles = Article.query.filter_by(owner=userid).all()
        return jsonify([(x.id,x.title) for x in all_articles])
    else:
        return jsonify({'aa','bb'})
        # with open('tree.json','r') as f:
        #     return f.read()
# 創建tree
def tree_create():
    pass
    
@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


# @app.route('/api/token')
# @auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/resource', methods=['POST'])
# @auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})



@app.route("/")
def normal():
    return jsonify("成功")

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    # if not os.path.exists('db.sqlite'):
    #     db.create_all()
    app.run(debug=True)
