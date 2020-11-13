from flask import Blueprint, jsonify, request, abort, g,url_for
from flasgger import swag_from

from apps import db
from apps.models.models import Article
from apps.auth.auth import verify_password

bp = Blueprint('article', __name__)
# 创建文章
@bp.route('/create', methods=['POST'])
@swag_from('../doc/article_create.yml')
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
@bp.route('/delete', methods= ['DELETE'])
@swag_from('../doc/article_delete.yml')
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
@bp.route('/update', methods=['PUT'])
@swag_from('../doc/article_update.yml')
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
@bp.route('/view', methods = ['POST'])
def article_view():
    if verify_password(request.headers.get('token')):
        userid = g.user.id
        all_articles = Article.query.filter_by(owner=userid).all()
        return jsonify([(x.id,x.title) for x in all_articles])
    else:
        return jsonify({'aa','bb'})
        # with open('tree.json','r') as f:
        #     return f.read()
      