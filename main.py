from bson.json_util import dumps
from flask import Flask,jsonify, request,make_response
from flask_restful import Resource,Api
from flask_pymongo import PyMongo
from flask_cors import CORS
import json
import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://db:27017/MyDatabase"
#app.config['MONGO_URI'] = "mongodb://localhost:27017/MyDatabase"
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)
mongo = PyMongo(app)
api = Api(app)


class Users(Resource):
    def get(self):
        userz = list(mongo.db.users.find({},{'_id':0}))
        # output = []
        # for i in userz:
        #     output.append({'username': i['username'], 'name': i['name'], 'phone_number': i['phone_number'], 'date': str( i['date'])})
        #resp = dumps(userz)
        return userz


class Role(Resource):
    def get(self):
        role = list(mongo.db.role.find({},{'_id':0}))
        # out = []
        # for i in role:
        #     out.append({'role': i['role'], 'date': str( i['date'])})
        return role

class Login(Resource):
    def post(self):
        try:
            username = request.json['username']
            password = request.json['password']
            userz = mongo.db.users.find_one({'username':username})
            if userz:
                if password == userz['password']:
                    #return make_response(json.dumps({'message': 'login succesfull'}
                    #result = {'username': userz['username'], 'name': userz['name'],'phone_number': userz['phone_number']}
                    result = {'username': userz['username']}
                    # if userz['role'] is not None:
                    #     final = {'username': userz['username'], 'name': userz['name'],'phone_number': userz['phone_number'],'role':userz['role']}
                    #     return final
                    # else:
                    #     return result
                    return result
            return make_response(json.dumps({'message': 'invalid credentials'}), 200)
        except:
            return make_response(json.dumps({'message': 'Internal Server Error'}), 500)


class Register(Resource):
    def post(self):
        try:
            username = request.json['username']
            password = request.json['password']
            name = request.json['name']
            phone_number = request.json['phone_number']
            #role = request.json['role']
            role = "null"
            date = str(datetime.datetime.now())
            userz = mongo.db.users.find_one({'username':username})
            if userz is None:
                id = mongo.db.users.insert({'username':username,'password':password,'name':name,'phone_number':phone_number, 'role':role ,'date':date})
                if id is not None:
                    return make_response(json.dumps({'message': 'Successfully registered'}), 200)
                else:
                    return make_response(json.dumps({'message':'registration failed'}),200)
            else:
                return make_response(json.dumps({'message': 'username already exists'}), 200)
        except:
            return make_response(json.dumps({'message':'internal server error'}),500)


class ChangePassword(Resource):
    def post(self):
        try:
            username = request.json['username']
            old_password = request.json['old_password']
            new_password = request.json['new_password']
            date = str(datetime.datetime.now())
            filter = {"username": username}
            update = {"$set": {"password": new_password , "date":date}}
            userz = mongo.db.users.find_one({'username': username })
            if userz:
                if old_password == userz['password']:
                    mongo.db.users.update_one(filter,update)
                    return make_response(json.dumps({'message': 'Password changed.'}), 200)
            return make_response(json.dumps({'message':'Invalid username and old password'}),200)
        except:
            return make_response(json.dumps({'message': 'Internal Server Error'}), 500)


class ForgotPassword(Resource):
    def post(self):
        try:
            username = request.json['username']
            phone_number = request.json['phone_number']
            new_password = request.json['new_password']
            date = str(datetime.datetime.now())
            userz = mongo.db.users.find_one({'username':username})
            if userz:
                if phone_number == userz['phone_number']:
                    mongo.db.users.update_one({"phone_number":phone_number},{"$set":{"password":new_password , "date":date}})
                    return make_response(json.dumps({'message': 'New Password set.'}), 200)
            return make_response(json.dumps({'message': 'Invalid username and old password'}), 200)
        except:
            return make_response(json.dumps({'message': 'Internal Server Error'}), 500)


class AddUser(Resource):
    def post(self):
        try:
            username = request.json['username']
            password = request.json['password']
            name = request.json['name']
            phone_number = request.json['phone_number']
            role = request.json['role']
            date = str(datetime.datetime.now())
            userz = mongo.db.users.find_one({'username':username})
            rolee = mongo.db.role.find_one({'role':role})
            if userz is None :
                if rolee is not None:
                    id = mongo.db.users.insert({'username':username,'name':name,'phone_number':phone_number,'password':password,'role':role , 'date': date})
                    if id is not None:
                        return make_response(json.dumps({'message': 'user created with role'}), 200)
                    else:
                        return make_response(json.dumps({'message': 'op failed'}), 200)
                else:
                    return make_response(json.dumps({'message': 'role doesnt exist'}), 200)
            else:
                return make_response(json.dumps({'message': 'User Already exists'}), 200)
        except:
            return make_response(json.dumps({'message': 'internal server error'}), 500)


class DeleteUser(Resource):
    def post(self):
        try:
            username = request.json['username']
            password = request.json['password']
            userz = mongo.db.users.find_one({'username': username})
            if userz:
                if password == userz['password']:
                    mongo.db.users.delete_one({'username':username})
                    return make_response(json.dumps({'message': 'User Deleted'}), 200)
                return make_response(json.dumps({'message':'invalid credentials'}))
            return make_response(json.dumps({'message': 'user doesnt exist'}), 200)
        except:
            return make_response(json.dumps({'message': 'internal server error'}), 500)


class AddRole(Resource):
    def post(self):
        try:
            role = request.json['role']
            date = str(datetime.datetime.now())
            rolee = mongo.db.role.find_one({'role':role})
            if rolee is None:
                id = mongo.db.role.insert({'role':role, 'date':date})
                if id is not None:
                    return make_response(json.dumps({'message': 'role registered'}), 200)
                else:
                    return  make_response(json.dumps({'message':'failed'}),200)
            else:
                return make_response(json.dumps({'message': 'role already exists'}), 200)
        except:
            return make_response(json.dumps({'message': 'internal server error'}), 500)


class EditRole(Resource):
    def post(self):
        try:
            role = request.json['role']
            new_role = request.json['new_role']
            date = str(datetime.datetime.now())
            rolee = mongo.db.role.find_one({'role': role})
            user_role = mongo.db.role.find({'role': role})
            if rolee is not None and user_role is None:
                result = mongo.db.role.update_one({'role':role}, {"$set":{"role":new_role , "date":date}})
                if result is not None:
                    return make_response(json.dumps({'message': 'role name updated'}), 200)
            return make_response(json.dumps({'message':'role doesnt exists OR already assigned to some user'}))
        except:
            return make_response(json.dumps({'message': 'internal server error'}), 500)



class DeleteRole(Resource):
    def post(self):
        try:
            role = request.json['role']
            rolee = mongo.db.role.find_one({'role': role})
            user_role = mongo.db.role.find({'role':role})
            if rolee is not None and user_role is None:
                result = mongo.db.role.delete_one({'role': role})
                if result is not None:
                    return make_response(json.dumps({'message': 'role removed'}), 200)
            return make_response(json.dumps({'message': 'role doesnt exists OR role already assigned to user'}), 200)
        except:
            return make_response(json.dumps({'message: internal server error'}), 500)


class AddUserRole(Resource):
    def post(self):
        try:
            username = request.json['username']
            role = request.json['role']
            date = str(datetime.datetime.now())
            userz = mongo.db.users.find_one({'username': username})
            rolee = mongo.db.role.find_one({'role':role})
            if userz:
                if rolee:
                    mongo.db.users.update_one({'username':username},{"$set":{"role":role, "date":date}})
                    return make_response(json.dumps({'message': 'role assigned'}), 200)
                return make_response(json.dumps({'message': 'role doesnt exists'}))
            return make_response(json.dumps({'message': 'user doesnt exist'}), 200)
        except:
            return make_response(json.dumps({'message': 'internal server error'}), 500)


class DeleteUserRole(Resource):
    def post(self):
        try:
            username = request.json['username']
            userz = mongo.db.users.find_one({'username': username})
            if userz:
            # role = userz['role']
            # if role is None:
            #     return make_response(json.dumps({'message':'user doesnt has any role'}))
            # else:
                result = mongo.db.users.update_one({'username': username}, {"$unset": {"role": ""}})
                if result is not None:
                    return make_response(json.dumps({'message': 'role removed'}), 200)
            return make_response(json.dumps({'message': 'user doesnt exists'}),200)
        except:
            return make_response(json.dumps({'message': 'internal server error'}), 500)


# class DeleteRole(Resource):
#     def post(self):
#         try:
#             username = request.json['username']
#             userz = mongo.db.users.find_one({'username': username})
#             if userz:
#                 result = mongo.db.users.update_one({'username': username}, {"$unset": {"role": ""}})
#                 if result is not None:
#                     return make_response(json.dumps({'message': 'role removed'}), 200)
#             return make_response(json.dumps({'message': 'user doesnt exists'}),200)
#         except:
#             return make_response(json.dumps({'message': 'internal server error'}), 500)


class Healtcheck(Resource):
    def get(self):
        return jsonify({"is_online":True})


api.add_resource(Register,'/register')
api.add_resource(Users,'/users')
api.add_resource(Role,'/role')
api.add_resource(Login,'/login')
api.add_resource(ChangePassword,'/change-password')
api.add_resource(ForgotPassword,'/forgot-password')
api.add_resource(AddUser,'/add-user')
api.add_resource(DeleteUser,'/delete-user')
api.add_resource(AddRole,'/add-role')
api.add_resource(EditRole,'/edit-role')
api.add_resource(DeleteRole,'/delete-role')
api.add_resource(AddUserRole,'/add-user-role')
api.add_resource(DeleteUserRole,'/delete-user-role')
api.add_resource(Healtcheck,"/health-check")

if __name__ == '__main__':
    app.run(host ='0.0.0.0',port=5000, debug=True)