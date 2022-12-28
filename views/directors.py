from flask_restx import Resource, Namespace
from flask import request
from dao.model.director import DirectorSchema
from implemented import director_service
from decorator import auth_required, admin_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200
    @admin_required
    def post(self):
        request_json = request.json
        director_service.create(request_json)
        return "", 201


@director_ns.route('/<int:rid>')
class DirectorView(Resource):

    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, id):
        request_json = request.json
        if "id" not in request_json:
            request_json["id"] = id

        director_service.update(request_json)
        return "", 204

    @admin_required
    def delete(self, id):
        director_service.delete(id)
        return "", 204



