import json
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import column_property, sessionmaker
from datetime import datetime
from flask import Flask, render_template, request, redirect, jsonify, url_for, Blueprint
from models import Restaurant, Base, User, Address, Rating, engine

userController = Blueprint('userController', __name__)


DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a new user
@userController.route('/users', methods=['POST'])
def newUser():

    userFirstName = request.get_json()["first_name"]
    userLastName = request.get_json()["last_name"]
    userPhone = request.get_json()["phone"]
    
    newUser = User(first_name=userFirstName, last_name=userLastName,phone=userPhone)

    try:
        session.add(newUser)
        session.commit()
        return "New User Added"
    except:
        session.rollback()
        session.flush()
        return "New User not added"


# Get all Users
@userController.route('/users' , methods=['GET'])
def showUsers():
    
    try:
    	users = list(session.query(User).all())

    	temp_stores = []
    	for user in users:
    
        	new_user = {
            'id':user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone':user.phone
        	}
        	temp_stores.append(new_user)

    
    	return jsonify({'users': temp_stores})
    except:
    	
        return "Check Url"

# Get User Info by ID
@userController.route('/users/<int:userId>' , methods=['GET'])
def showUserByUserId(userId):
    try:
    	users = list(session.query(User).filter(User.user_id==userId).all())

    	temp_stores = []
    	for user in users:
    
        	new_user = {
            'id':user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone':user.phone
        	}
        	temp_stores.append(new_user)

    
    	return jsonify({'users': temp_stores})
    except:
    	
        return "User with Id %s not Found" % (userId)


# Update a user
@userController.route('/users/<int:userId>', methods=['PUT'])
def updateUser(userId):
    
    try:
        userToUpdate = session.query(User).filter(User.user_id==userId).one()

        userToUpdate.first_name = request.get_json()["first_name"]
        userToUpdate.last_name = request.get_json()["last_name"]
        userToUpdate.phone = request.get_json()["phone"]
        session.commit()
        return "User Updated"

    except:
    	
        session.rollback()
        return "User with Id %s not Found" % (userId)


# Delete a user
@userController.route('/users/<int:userId>', methods=['DELETE'])
def deleteUser(userId):
    
    try:
        userToDelete = session.query(User).filter(User.user_id==userId).one()
        session.delete(userToDelete)
        session.commit()
        return "User Deleted"

    except:
        session.rollback()
        return "User with Id %s not Found" % (userId)