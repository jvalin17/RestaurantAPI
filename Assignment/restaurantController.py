import json
import sys
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import column_property, sessionmaker
from datetime import datetime
from flask import Flask, render_template, request, redirect, jsonify, url_for, Blueprint
from models import Restaurant, Base, User, Address, Rating, engine

restaurantController = Blueprint('restaurantController', __name__)

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a new restaurant
@restaurantController.route('/restaurants', methods=['POST'])
def newRestaurant():
    
    '''
    {
    "name" : "Drums",
    "category" : "Italian",
    "street" : "254 PLX St.",
    "city" : "Arlington",
    "state" : "TX",
    "zipcode" : 75043

    }
    '''

    
    restaurantName = request.get_json()["name"]
    categoryName = request.get_json()["category"]

    street = request.get_json()["street"]
    city = request.get_json()["city"]
    state = request.get_json()["state"]
    zipcode = request.get_json()["zipcode"]

    try:
    	restaurant_exists = session.query(Restaurant).filter(Restaurant.restaurant_name == restaurantName).scalar() is not None
    	address_exists = session.query(Address).filter(Address.address == street,Address.city == city,Address.state == state,Address.zipcode==zipcode).scalar() is not None     

    except ValueError:
    	return ("Unexpected error:", sys.exc_info()[0])


    if restaurant_exists :
            if address_exists:
                return 'Restaurant Already Exists'
            else:
                newAddress = Address (address=street,city=city,state=state,zipcode=zipcode,restaurant_name=restaurantName)
                session.add(newAddress)
                session.commit()
                return "New Retaurant added"
    else:
            newRestaurant = Restaurant(restaurant_name=restaurantName,restaurant_category=categoryName)
            newAddress = Address (address=street,city=city,state=state,zipcode=zipcode,restaurant_name=newRestaurant.restaurant_name)
            
            session.add(newRestaurant)
            session.add(newAddress)
            session.commit()
            return "New Retaurant added"

    
# Read/Show All Restaurants with or without filters
@restaurantController.route('/restaurants', methods=['GET'])
def showRestaurants():
    
    name = request.args.get('name')
    category = request.args.get('category')
    city = request.args.get('city')
    zipcode = request.args.get('zipcode')
    total_score = request.args.get('total_score')

    stores = []

    if city == None and total_score == None and category == None and zipcode == None:


        restaurants = list(session.query(Restaurant).all())
        
        for restaurant in restaurants:


            addresses = list(session.query(Address).filter(Address.restaurant_name==restaurant.restaurant_name))

            for address in addresses:
    
                new_restaurant = {
                'restaurant_name': restaurant.restaurant_name,
                'category': restaurant.restaurant_category,
                'address_id': address.address_id,
                'street': address.address,
                'city':address.city,
                'state':address.state,
                'zipcode':address.zipcode
                }
            
                stores.append(new_restaurant)

        return jsonify({'restaurants': stores})

    else:
    	stores = []
    	qry = session.query(Restaurant, Address, Rating).filter(Restaurant.restaurant_name == Address.restaurant_name ).\
                    filter(Address.address_id == Rating.address_id)

        if name != None:
        	print name
    		qry = qry.filter(Restaurant.restaurant_name == name)

    	if category != None:
    		print category
    		qry = qry.filter(Restaurant.restaurant_category == category)

    	if city != None:
    		qry = qry.filter(Address.city == city)

    	if zipcode != None:
    		qry = qry.filter(Address.zipcode == zipcode)

    	if total_score != None:
    		qry = qry.filter(Rating.total_score >= total_score)



    	result = qry.group_by(Address.address_id).all()
    

    	for Res, Add, Rat in result:
    		new_restaurant = {
                'restaurant_name': Res.restaurant_name,
                'category': Res.restaurant_category,
                'address_id': Add.address_id,
                'street': Add.address,
                'city':Add.city,
                'state':Add.state,
                'zipcode':Add.zipcode,
                'ratings':Rat.total_score
                }
        	stores.append(new_restaurant)

    	return jsonify({'restaurants': stores})
    

# Update a Restaurant
@restaurantController.route('/restaurants/<int:addressId>', methods=['PUT'])
def updateRestaurant(addressId):

	try:
		restaurant_category = request.get_json()["category"]
		street = request.get_json()["street"]
		city = request.get_json()["city"]
		state = request.get_json()["state"]
		zipcode = request.get_json()["zipcode"]
	except:
		return "Wrong Input"

	try:

		restaurantsToUpdate = session.query(Restaurant).filter(Restaurant.restaurant_name == Address.restaurant_name).filter(Address.address_id == addressId)
		addressesToUpdate = session.query(Address).filter(Address.address_id==addressId)

		for restaurant in restaurantsToUpdate:
			if restaurant_category != None:
				restaurant.restaurant_category = restaurant_category


		for address in addressesToUpdate:
			if street != None:
				address.address = street
			if city != None:
				address.city = city
			if state != None:
				address.state = state
			if zipcode != None:
				address.zipcode = zipcode

		session.commit()
		return "Restaurant Updated"
	except:
		session.rollback()
		return "Restaurant not Found"