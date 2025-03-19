from flask import Blueprint , request,session,jsonify
from databases.db import db
from databases.friends_db import *

friend_page = Blueprint("friends",__name__)

#create friend and get all friends
@friend_page.route("/api/friends/",methods = ["POST","GET"])
def create_friend():
    if request.method=='POST':
        data = request.json
        #validate data
        required_fields = ["name", "role", "description", "gender"]

        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"'{field}' field is required."}), 400

        name = data.get("name")
        role = data.get("role")
        desc = data.get("description")
        gender = data.get("gender")
    
        if gender== "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        else :
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        
        new_friend = Friend(name=name, role=role, desc=desc, gender= gender, img_url=img_url)
        db.session.add(new_friend)
        db.session.commit()
        return jsonify(new_friend.to_json()), 201
    else :
        friends = Friend.query.all()
        result = []
        for friend in friends:
            result.append(friend.to_json())
        return jsonify(result)
    
# delete friend
@friend_page.route("/api/friends/delete/<int:id>",methods = ["PATCH"])
def delete_friend(id):
    try:
        friend = Friend.query.filter_by(id= id).all()[0]
    except IndexError:  # if user not found
        return jsonify({"error":"Friend not found"}), 404
    
    db.session.delete(friend)
    db.session.commit()
    return jsonify({"msg":"Friend deleted"}), 200

#update
@friend_page.route("/api/friends/update/<int:id>",methods = ["POST"])
def update(id):
    try:
        friend = Friend.query.filter_by(id= id).all()[0]
    except IndexError:  # if user not found
        return jsonify({"error":"Friend not found"}), 404
    
    data = request.json
    
    friend.name = data.get("name",friend.name)
    friend.role = data.get("role",friend.role)
    friend.desc = data.get("description",friend.desc)
    friend.gender = data.get("gender",friend.gender)

    db.session.commit()
    return jsonify(friend.to_json()),200




