from flask_restplus import Resource, reqparse
import logging

from app.api.restplus import api
from app.encrypt.encrypt import encode
from app.response import response as resp

logger = logging.getLogger(__name__)

ns = api.namespace("auth", description="Endpoints for user auth")


parser = reqparse.RequestParser()
parser.add_argument("username", required=True)
parser.add_argument("password", required=True)

@ns.route("/login")
class Login(Resource):
    def post(self):
        try:
            parse_data = parser.parse_args()
        except:
            return resp.error("username, password must be specified")
        token = encode(**parse_data)
        return resp.success({
            "access_token": token
        })
