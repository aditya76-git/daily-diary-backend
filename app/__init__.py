from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from .routes.auth import auth as auth_blueprint
from .routes.user import user as user_blueprint
from .routes.streak import streak as streak_blueprint
from flask_jwt_extended import JWTManager
from .models import User


app = Flask(__name__)


jwt = JWTManager()
jwt.init_app(app)

app.config.from_object('config.Config')
app.secret_key = Config.APP_SECRET_KEY


app.register_blueprint(auth_blueprint, url_prefix = "/auth")
app.register_blueprint(user_blueprint, url_prefix = "/user")
app.register_blueprint(streak_blueprint, url_prefix = "/streak")

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify(
        {
            "error" : True,
            "message" : "Token Expired"
        }
    ), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify(
        {
            "error" : True,
            "message" : "Signature verification failed. Invalid token"
        }
    ), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify(
        {
            "error" : True,
            "message" : "Request doesn't contain valid token"
        }
    ), 401

@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    return {
            "is_admin" : True if identity == Config.ADMIN_USERNAME else False
    }

@jwt.user_lookup_loader
def user_lookup_callback(jwt_headers, jwt_data):
    username = jwt_data['sub']
    
    user = User().get_user_info(username)
    return user


CORS(app)