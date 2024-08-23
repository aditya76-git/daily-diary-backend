from ..models import Streak
from flask_jwt_extended import current_user
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

streak = Blueprint("streak", __name__)

@streak.route("/check", methods=["GET"])
@jwt_required()
def available_streak():
        return jsonify(Streak(current_user.get('username')).check()), 200



@streak.route("/add", methods=["GET"])
@jwt_required()
def add_streak():
        return jsonify(Streak(current_user.get('username')).add()), 200

