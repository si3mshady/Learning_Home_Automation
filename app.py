from flask import Flask
from flask_restful import  Resource, Api, reqparse
from flask_jwt_simple import  JWTManager, jwt_required, create_jwt

app=application=Flask(__name__)
api=Api(app)

app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'forTestingPurposes-si3mshady'
jwt = JWTManager(app)

devices = users_list = []
function_map = {obj.friendly_name: obj for obj in devices}

class Users():
    def __init__(self,username: str, pw: str):
        self.username = username
        self.pw = pw

    def __repr__(self):
        return f"Registered user {self.username}"

class Devices():
    def __init__(self,lambda_name: str, arn: str, region: str, friendly_name: str):
        self.lambda_name = lambda_name
        self.arn = arn
        self.region = region
        self.friendly_name = friendly_name

    def __repr__(self):
        return f"Connected Alexa Device object named {self.friendly_name}"

def getDeviceByFriendlyName(fn: str):
    '''use filter function to apply/iterate each list object in 'devices' which is
     a dictionary consisting of key=string:value=DeviceObject --  use 'next' method to retrieve
     first match from resultant filter obj - excellent!'''
    item = next(filter(lambda object: object.friendly_name == fn, devices), None)
    return item

def checkUserExists(username: str):
    function_map = {obj.username: obj for obj in users_list}
    if username in function_map:
        return True
    else:
        return False

class Register(Resource):
    def post(self):
        '''create reqparse obj and define args - create new user '''
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="This field is required")
        parser.add_argument('pw', type=str, required=True, help="This field is required")
        user_data = parser.parse_args()
        if not checkUserExists(user_data['username']):
            new_user = Users(**user_data)
            users_list.append(new_user)
            return {"message": f"Thank you for registering {new_user.username}"} , 201
        else:
            return {"message": f"User name {user_data['username']} is already registered"}, 203

class Login(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, required=True, help="This field is required")
            parser.add_argument('pw', type=str, required=True, help="This field is required")
            user_data = parser.parse_args()
            if checkUserExists(user_data['username']):
                jwt = create_jwt(identity=user_data['username'])
                return {"message": jwt}, 200
            else:
                return {"message": "You must register before you may login"}, 200

class Alexa_Device(Resource):
    @jwt_required
    def get(self,device_name: str):
        '''create k/v pair mapping friendly-name to instance object'''
        function_map = {obj.friendly_name: obj for obj in devices}
        if device_name in function_map:
            device = function_map[device_name]
            return {"name": device.friendly_name, "function_name": device.lambda_name}, 200 if device else 404

    @jwt_required
    def post(self,device_name: str):
        if getDeviceByFriendlyName(device_name):
            return {"message": f"A device named {device_name} exists"}
        parser = reqparse.RequestParser()
        parser.add_argument('lambda_name',type=str,required=True,help="This field is required")
        parser.add_argument('arn', type=str,required=True,help="This field is required")
        parser.add_argument('region', type=str,required=True,help="This field is required")
        parser.add_argument('friendly_name', type=str,required=True,help="This field is required")
        data = parser.parse_args()
        '''keyword args mapped to params of Device class'''
        device = Devices(**data)
        devices.append(device)
        return {"message": device_name +  " has been added to registry " }, 200 if device else 404

class Delete(Resource):
    @jwt_required
    def delete(self,device_name):
        function_map = {obj.friendly_name: obj for obj in devices}
        try:
            if device_name in function_map:
                object = function_map[device_name]
                devices.remove(object)
                del function_map[device_name]
                return {"message": device_name +  " has been deleted from registry " }, 200
        except KeyError:
            return {"message": "Key Error"}, 400

class Put(Resource):
    @jwt_required
    def put(self,device_name):
        if  getDeviceByFriendlyName(device_name):
            item = getDeviceByFriendlyName(device_name)
            parser = reqparse.RequestParser()
            parser.add_argument('lambda_name', type=str, required=True, help="This field is required")
            parser.add_argument('arn', type=str, required=True, help="This field is required")
            parser.add_argument('region', type=str, required=True, help="This field is required")
            parser.add_argument('friendly_name', type=str, required=True, help="This field is required")
            data = parser.parse_args()
            '''keyword args mapped to params of Device class'''
            device = Devices(**data)
            devices.append(device)
            return {"message": device_name + " has been updated "}, 200 if device else 404
        elif not getDeviceByFriendlyName(device_name):
            parser = reqparse.RequestParser()
            parser.add_argument('lambda_name', type=str, required=True, help="This field is required")
            parser.add_argument('arn', type=str, required=True, help="This field is required")
            parser.add_argument('region', type=str, required=True, help="This field is required")
            parser.add_argument('friendly_name', type=str, required=True, help="This field is required")
            data = parser.parse_args()
            '''keyword args mapped to params of Device class'''
            device = Devices(**data)
            devices.append(device)
            return {"message": device_name + " has been added to registry "}, 200 if device else 404



api.add_resource(Register,'/user/register')
api.add_resource(Login,'/user/login')
api.add_resource(Alexa_Device,'/device/<device_name>')
api.add_resource(Delete,'/delete/<device_name>')
api.add_resource(Put,'/device/put/<device_name>')

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)

#Flask_Restful CRUD practice - updating Alexa device registry
# using JWT auth, classes and lambdas learning to better use lambdas and classes when implementing api's
#Elliott Arnold 10-6-2019