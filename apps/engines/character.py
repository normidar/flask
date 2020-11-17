from flask import Blueprint, jsonify, request, g
from flasgger import swag_from

from apps import db
from apps.models.character import Character
from apps.engines.auth import verify_password

bp = Blueprint('character', __name__)
swag_path = '../doc/character/'
# 创建角色
@bp.route('/create', methods=['POST'])
@swag_from(swag_path+'create.yml')
def character_create():
    name = request.values.get('name')
    can_edit_article = request.values.get('can_edit_article')
    can_edit_tree = request.values.get('can_edit_tree')
    # 登录了才可以
    if verify_password(request.headers.get('token')):
        if g.user.character_id == 1:
            new_chara = Character(
                name = name,
                can_edit_article = bool(can_edit_article),
                can_edit_tree = bool(can_edit_tree),
            )
            db.session.add(new_chara)
            db.session.commit()
            return jsonify({'success':'sdf'})
        else:
            return jsonify({'fail':'you are a low low'})
    else:
        return jsonify({'fail':'no login'})

# 删除角色
@bp.route('/del', methods=['DELETE'])
@swag_from(swag_path+'del.yml')
def character_del():
    id = request.values.get('id')
    # 登录了才可以
    if verify_password(request.headers.get('token')):
        if g.user.character_id == 1:
            if id > 2:
                Character.query.filter_by(id=id).delete()
                db.session.commit()
                return jsonify({'success':id})
            else:
                return jsonify({'fail':'can not delete 1,2'})
        else:
            return jsonify({'fail':'you are a low low'})
    else:
        return jsonify({'fail':'no login'})

#更改角色
@bp.route('/update', methods=['PUT'])
@swag_from(swag_path+'update.yml')
def character_update():
    id = request.values.get('id')
    name = request.values.get('name')
    can_edit_article = request.values.get('can_edit_article')
    can_edit_tree = request.values.get('can_edit_tree')
    # 登录了才可以
    if verify_password(request.headers.get('token')):
        # 管理员才可以
        if g.user.character_id == 1:
            # 只能动大于2的角色
            if id > 2:
                update_map = {}
                if name != "": update_map['name'] =name
                if can_edit_article != "": update_map['can_edit_article'] =can_edit_article
                if can_edit_tree != "": update_map['can_edit_tree'] = can_edit_tree
                Character.query.filter_by(id=id).update(update_map)
                db.session.commit()
                return jsonify({'success':id})
            else:
                return jsonify({'fail':'can not delete 1,2'})
        else:
            return jsonify({'fail':'you are a low low'})
    else:
        return jsonify({'fail':'no login'})
