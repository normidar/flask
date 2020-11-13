from model import jsonify,db
import auth
import article
from tree import app
    
# @app.route('/api/users/<int:id>')
# def get_user(id):
#     user = User.query.get(id)
#     if not user:
#         abort(400)
#     return jsonify({'username': user.username})


# # @app.route('/api/token')
# # @auth.login_required
# def get_auth_token():
#     token = g.user.generate_auth_token(600)
#     return jsonify({'token': token.decode('ascii'), 'duration': 600})


# @app.route('/api/resource', methods=['POST'])
# def get_resource():
#     return jsonify({'data': 'Hello, %s!' % g.user.username})



@app.route("/")
def normal():
    return jsonify("success")

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    # if not os.path.exists('db.sqlite'):
    #     db.create_all()
    app.run(debug=True)
