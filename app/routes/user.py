from flask_jwt_extended import current_user
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from datetime import datetime
from ..models import Entry, Category
from ..utils import extract_emojis, generate_tokens, encrypt

user = Blueprint("user", __name__)

@user.route("/info", methods=["GET"])
@jwt_required()
def user_info():
        return jsonify({
            "error": False,
            "message": "User details fetched successfully",
            "details" : {
                "username" : current_user.get('username'),
                "email" : current_user.get('email'),
                "profilePicture" : current_user.get('profile_picture'),
                "categories" : current_user.get('categories'),
                "userId" : current_user.get('user_id'),
                "createdAt" : current_user.get('created_at'),
            }
    }), 200



@user.route("/add-category", methods=["POST"])
@jwt_required()
def add_category():
        data = request.get_json()
        print(data)
        category = Category()

        add_category_dict = {
            "username" : current_user.get('username'),
            "category_name" : data.get('category').strip(),
        }

        category_add_operation_status = category.add(
            **add_category_dict
        )
        return jsonify({
            "error": not category_add_operation_status,
            "message": "Category {} added successfully".format(
                    data.get('category').strip() if category_add_operation_status else "Something went wrong"
            ),
    }), 200

@user.route("/add-entry", methods=["POST"])
@jwt_required()
def add_entry():
        now = datetime.now()

        data = request.get_json()
        entry = Entry()

        add_entry_dict = {
            "username" : current_user.get('username'),
            "title" : encrypt(data.get('title').strip()),
            "description" : encrypt(data.get('description').strip()),
            "emoji" : extract_emojis(data.get('emoji')),
            "category" : data.get('categories'),
            "sharing" : data.get('sharing'),
            "slug" : data.get('slug'),
        }
        
        search_token = generate_tokens(data.get('title').strip())

        add_entry_dict['title_search_token'] = search_token

        add_entry_dict['year'] = now.year
        add_entry_dict['month'] = now.month
        add_entry_dict['day'] = now.day

        print(add_entry_dict)
        

        entry_add_operation_status = entry.add(
            **add_entry_dict
        )
        return jsonify({
            "error": not entry_add_operation_status,
            "message": "Post added successfully" if entry_add_operation_status else "Something went wrong",
    }), 200



@user.route("/edit-entry", methods=["POST"])
@jwt_required()
def edit_entry():

        data = request.get_json()

        entry = Entry()

        edit_entry_dict = {
            "post_id" : data.get('postId'),
            "category" : data.get('categories'),
            "sharing" : data.get('sharing'),
            "slug" : data.get('slug')
        }
        

        if data.get('title'):
            edit_entry_dict['title'] = encrypt(data.get('title').strip())
            edit_entry_dict['title_search_token'] = generate_tokens(data.get('title').strip())
        
        if data.get('description'):
            edit_entry_dict['description'] = encrypt(data.get('description').strip())

        if data.get('emoji'):
            edit_entry_dict['emoji'] = extract_emojis(data.get('emoji'))
        

        edit_operation_status = entry.edit(
            **edit_entry_dict
        )
        return jsonify({
            "error": not edit_operation_status,
            "message": "Post updated successfully" if edit_operation_status else "Something went wrong",
    }), 200



@user.route("/list-entries", methods=["GET"])
@jwt_required()
def list_entries():
        query = request.args.get('query')
        entry = Entry()


        entries = entry.get(
                username = current_user.get('username'), query = query
        )


        return jsonify({
            "error": False,
            "message": "Entries fetched successfully",
            "entries" : entries
    }), 200