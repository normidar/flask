from model import *
import json
# 創建tree
@app.route('/api/v1/tree/create', methods= ['POST'])
def tree_create():
    id = int(request.values.get('id'))
    name = request.values.get('name')
    json_str = ""
    with open('codes/tree.json','r') as f:
        json_str = f.read()
    tree_map = json.loads(json_str)
    create_tree(tree_map, id,name,tree_map['max']+1)
    tree_map['max']+=1
    with open('codes/tree.json','w') as f:
        f.write(json.dumps(tree_map))
    # return jsonify(find_tree_id(tree_map, id))
    return jsonify(tree_map)

def find_tree_id(tree_map:dict,id):
    for k in tree_map.keys():
        if k == 'id' and tree_map[k] == id:
            return tree_map['name']
        if k != 'id' and k != 'name':
            has = find_tree_id(tree_map[k],id)
            if has != None:
                return has
    return None
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
@app.route('/api/v1/tree/view', methods= ['POST','GET'])
def tree_view():
    with open('codes/tree.json','r') as f:
        return f.read()
    

# 削除tree
def tree_delete():
    pass

# 更改tree
def tree_update():
    pass