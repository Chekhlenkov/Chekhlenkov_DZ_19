from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service
from decorator import auth_required, admin_required

user_ns = Namespace("users")

@user_ns.route("/")
class UsersView(Resource):

    def get(self):
        all_users = user_service.get_all()
        result = UserSchema(many=True).dump(all_users)
        return result, 200


    def post(self):
        request_json = request.json
        user = user_service.create(request_json)
        return "", 201, {"location": f"/user/{user.id}"}

    @user_ns.route("/<int:id>")
    class UserView(Resource):
        def get(self, id):
            user = user_service.get_one(id)
            result = UserSchema().dump(user)
            return result, 200


        def patch(self, id):
            request_json = request.json
            if "id" not in request_json:
                request_json["id"] = id

            user_service.update(request_json)
            return "", 204


        def delete(self, id):
            user_service.delete(id)
            return "", 204

    @user_ns.route("/password")
    class UpdateUserPasswordViews(Resource):
        def put(self):
            data = request.json
            email = data.get("email")
            old_password = data.get("old_password")
            new_password = data.get("new_password")
            user = user_service.get_user_by_email(email)
            if user_service.compare_passwords(user.password, old_password):
                user.password = user_service.make_user_password_hash(new_password)
                result = UserSchema().dump(user)
                user_service.update(result)
                print("Пароль обновлён")
            else:
                print("Пароль не обновлён")
            return "", 201

