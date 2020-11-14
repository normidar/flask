from flask import Blueprint, jsonify, request, abort, g,url_for
from flasgger import swag_from

from apps import db
from apps.models.models import Article
from apps.engines.auth import verify_password
import json

path = 'tree.json'
swag_path = '../doc/tree_'

bp = Blueprint('tree', __name__)
# 創建tree
@bp.route('/create', methods= ['POST'])
@swag_from(swag_path+'create.yml')
def tree_create():
    id = int(request.values.get('id'))
    name = request.values.get('name')
    # json_str = ""
    with open(path,'r') as f:
        json_str = f.read()
    tree_map = json.loads(json_str)
    create_tree(tree_map, id,name,tree_map['max']+1)
    tree_map['max']+=1
    with open(path,'w') as f:
        f.write(json.dumps(tree_map))
    # return jsonify(find_tree_id(tree_map, id))
    return jsonify(tree_map)

# def find_tree_id(tree_map:dict,id):
#     for k in tree_map.keys():
#         if k == 'id' and tree_map[k] == id:
#             return tree_map['name']
#         if k != 'id' and k != 'name':
#             has = find_tree_id(tree_map[k],id)
#             if has != None:
#                 return has
#     return None
def create_tree(tree_map:dict,id,insert_name,insert_id):
    for k in tree_map.keys():
        if k == 'id' and tree_map[k] == id:
            tree_map[insert_name] = {
                "id":insert_id,
                "name":insert_name
            }
            return tree_map
        if k != 'id' and k != 'name' and k != 'max':
            has = create_tree(tree_map[k],id,insert_name,insert_id)
            if has != None:
                tree_map[k] = has
    return None

# 查看树
@bp.route('/view', methods= ['GET'])
@swag_from(swag_path+'view.yml')
def tree_view():
    with open(path,'r') as f:
        return f.read()
    

# 削除tree
@bp.route('/del', methods= ['DELETE'])
def tree_delete():
    id = int(request.values.get('id'))
    with open(path,'r') as f:
        json_str = f.read()
    tree_map = json.loads(json_str)
    suc =  del_tree(tree_map,id)
    if suc != None:
        with open(path,'w') as f:
            f.write(json.dumps(tree_map))
        return jsonify(tree_map)
    else:
        return jsonify({"fail":"sb"})

def del_tree(tree_map:dict,id):
    if id != 0:
        for k in tree_map.keys():
            # if k == 'id' and tree_map[k] == id:
            #     return tree_map['name']
            if k != 'id' and k != 'name' and k != 'max':
                son_id = tree_map[k]['id']
                if son_id == id:
                    tree_map.pop(k)
                    return tree_map
                has = del_tree(tree_map[k],id)
                if has != None:
                    tree_map[k] = has
                    return tree_map
    return None

# 更改tree
@bp.route('/update', methods= ['PUT'])
def tree_update():
    id = int(request.values.get('id'))
    name = request.values.get('name')
    with open(path,'r') as f:
        json_str = f.read()
    tree_map = json.loads(json_str)
    suc =  update_tree(tree_map,id,name)
    if suc != None:
        # with open(path,'w') as f:
        #     f.write(json.dumps(tree_map))
        return jsonify(tree_map)
    else:
        return jsonify({"fail":"sb"})

def update_tree(tree_map:dict,id,name):
    if id != 0:
        for k in tree_map.keys():
            # if k == 'id' and tree_map[k] == id:
            #     return tree_map['name']
            if k != 'id' and k != 'name' and k != 'max':
                son_id = tree_map[k]['id']
                if son_id == id:
                    tree_map[name] = tree_map.pop(k)
                    tree_map[name]['name'] = name
                    return tree_map
                has = update_tree(tree_map[k],id,name)
                if has != None:
                    tree_map[k] = has
                    return tree_map
    return None