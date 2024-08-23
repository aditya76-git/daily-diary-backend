import re
import requests
import json
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request, redirect
from ..models import User
from ..utils import get_google_provider_cfg, base64_encode
from ..auth import google_client
from config import Config

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    required_fields = ['username', 'password', 'email']
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({
            "error": True,
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    
    email = data['email']

    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return jsonify({
            "error": True,
            "message": "Invalid email address."
        }), 400

    user = User().get_user(
        username = data.get('username')
    )

    if user is not None:
        return jsonify(
            {
                "error" : True,
                "message" : "Username already exists"
            }
        ), 200
    
    add_user_operation_status = User().add_user(**data)

    return jsonify(
        {
            "error" : not add_user_operation_status,
            "message" : "User added successfully" if add_user_operation_status else "Something went wrong adding user"
        }
    ), 400

@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    required_fields = ['username', 'password']
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({
            "error": True,
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    
    user = User().get_user(
        username = data.get('username')
    )

    if user and User().check_password_hash(
        data.get('password'),
        user.get('password')
    ):

        access_token = create_access_token(
            identity = data.get('username'),
        )
        refresh_token = create_refresh_token(
            identity = data.get('username'),
        )

        return jsonify(
            {
                "error" : False,
                "message" : "Logged in successfully",
                "tokens" : {
                    "access" : access_token,
                    "refresh" : refresh_token
                }
            }
        ), 200
    
    return jsonify({
        "error" : True,
        "message" : "Invalid username or password"
    }), 400


@auth.route("/login/google", methods=["GET", "POST"])
def google_login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    try:

        request_uri = google_client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri = request.base_url + "/callback",
            scope = ["openid", "email", "profile"],
        )

        error = False
        message = "Redirect URL generated successfully"
        
    except Exception as e:
        error = True
        message = str(e)
        request_uri = None

    return jsonify(
        {
            "error" : error,
            "message" : message,
            "link" : request_uri
        }
    )

@auth.route("/login/google/callback")
def google_callback():
    
    code = request.args.get("code")
    print(code)

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = google_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url= request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    google_client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = google_client.add_token(userinfo_endpoint)

    userinfo_response = requests.get(uri, headers=headers, data=body).json()

    google_username = userinfo_response['email'].split("@")[0]

    user = User().get_user(
        username = google_username
    )

    if user is None:
        User().add_google_user(
            userinfo_response['email'],
            google_username,
            userinfo_response.get('picture')
        )

        
    access_token = create_access_token(
        identity = google_username,
    )
    refresh_token = create_refresh_token(
        identity = google_username,
    )

    
    data = {
        "error" : False,
        "message" : "Logged in successfully",
        "tokens" : {
            "access" : access_token,
            "refresh" : refresh_token
        }
    }

    return redirect(
        Config.CLIENT_CALLBACK_REDIRECT_URL + "?code=" + base64_encode(str(data))
    )



@auth.route("/refresh", methods=["GET"])
@jwt_required(refresh = True)
def refresh_token():
    identity = get_jwt_identity()
    new_access_token = create_access_token(
        identity = identity 
    )

    return jsonify(
        {
            "error" : False,
            "message" : "Access token refreshed successfully",
            "access_token" : new_access_token
        }
    )