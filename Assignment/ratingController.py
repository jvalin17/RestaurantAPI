import json
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import column_property, sessionmaker
from datetime import datetime
from flask import Flask, render_template, request, redirect, jsonify, url_for, Blueprint
from models import Restaurant, Base, User, Address, Rating, engine

ratingController = Blueprint('ratingController', __name__)

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a rating
@ratingController.route('/ratings', methods=['POST'])
def newRating():
    
    try:
    	user_id = request.get_json()["user_id"]
    	address_id = request.get_json()["address_id"]
    	restaurant_name = request.get_json()["restaurant_name"]
    	cost_rating = request.get_json()["cost_rating"]
    	food_rating = request.get_json()["food_rating"]
    	cleanliness_rating = request.get_json()["cleanliness_rating"]
    	service_rating = request.get_json()["service_rating"]
    	total_score = (cost_rating + food_rating + cleanliness_rating + service_rating)/4

    	user_ratings = list(session.query(Rating).filter (Rating.user_id == user_id).filter (Rating.address_id == address_id).all())
    
    	if cost_rating > 5 or cost_rating < 1 or food_rating > 5 or food_rating < 1 or cleanliness_rating > 5 or cleanliness_rating < 1 or service_rating > 5 or service_rating < 1:
    		return "Please Give Rating in Range 1 to 5"



    	if len(user_ratings) > 0:
    		return "Rating for this location already Exists, Try Updating it"

    	else:
    		user_exists = session.query(User).filter(User.user_id == user_id).scalar() is not None
    		address_exists = session.query(Address).filter(Address.address_id == address_id).scalar() is not None

    
    	if user_exists and address_exists:

    		newRating = Rating(user_id=user_id, address_id=address_id,restaurant_name=restaurant_name, cost_rating=cost_rating,
        	food_rating=food_rating, cleanliness_rating=cleanliness_rating,service_rating=service_rating,total_score=total_score )

    	else:
    		return "Either user or address doesn't exist"
    except:
    	return "Wrong Input"
	
    try:
        session.add(newRating)
        session.commit()
        return "New Rating Added"

    except:
        session.rollback()
        session.flush()
        return "New Rating not added"

#Show All Ratings
@ratingController.route('/ratings', methods=['GET'])
def showRatings():
    rating_store = []
    
    for Res, Add, Rat in session.query(Restaurant, Address, Rating).filter(Restaurant.restaurant_name == Address.restaurant_name ).\
                    filter(Address.address_id == Rating.address_id).\
                    filter(Restaurant.restaurant_name==Rating.restaurant_name).\
                    all():

            show_rating = {
                'user_id': Rat.user_id,
                'restaurant_name': Rat.restaurant_name,
                'restaurant_category':Res.restaurant_category,
                'address_id': Rat.address_id,
                'street':Add.address,
                'city':Add.city,
                'zipcode':Add.zipcode,
                'date': Rat.date,
                'cost_rating':Rat.cost_rating,
                'food_rating':Rat.food_rating,
                'cleanliness_rating':Rat.cleanliness_rating,
                'service_rating':Rat.service_rating,
                'total_score':Rat.total_score
                }
            
            rating_store.append(show_rating)

    
    return jsonify({'ratings': rating_store})

#Show All Ratings for a User
@ratingController.route('/ratings/user=<int:userId>', methods=['GET'])
def showRatingByUserId(userId):

	users = list(session.query(Rating).filter(Rating.user_id==userId).all())
	rating_store = []

	for user in users:
		for Res, Add, Rat in session.query(Restaurant, Address, Rating).filter(Restaurant.restaurant_name == Address.restaurant_name ).\
    		filter(Address.address_id == Rating.address_id).\
    		filter(Restaurant.restaurant_name==Rating.restaurant_name).\
    		filter(Rating.user_id == user.user_id).\
    		all():
    		
    			show_rating={                
    			'user_id': Rat.user_id,
                'restaurant_name': Rat.restaurant_name,
                'restaurant_category':Res.restaurant_category,
                'address_id': Rat.address_id,
                'street':Add.address,
                'city':Add.city,
                'zipcode':Add.zipcode,
                'date': Rat.date,
                'cost_rating':Rat.cost_rating,
                'food_rating':Rat.food_rating,
                'cleanliness_rating':Rat.cleanliness_rating,
                'service_rating':Rat.service_rating,
                'total_score':Rat.total_score
                	}

        		rating_store.append(show_rating)
	
	return jsonify({'ratings': rating_store})


#Show All Ratings for a Restaurant Address Id 
@ratingController.route('/ratings/address=<int:addressId>', methods=['GET'])
def showRatingByRestaurantAddressId(addressId):
	
	try:
		restaurant_ratings = session.query(Rating.address_id.label('address_id'), \
		Rating.restaurant_name.label('restaurant_name'), Address.address.label('address'),\
		Address.city.label('city'),Address.state.label('state'),\
		func.avg(Rating.total_score).label('average')).\
		filter(Rating.address_id==addressId).filter(Address.address_id == addressId ).\
		group_by(Rating.address_id).all()
	
		rating_store = []

		for rating in restaurant_ratings:
			show_rating={                
    			
                'restaurant_name': rating.restaurant_name,
                'address_id': rating.address_id,
                'street':rating.address,
                'city':rating.city,
                'state':rating.state,
                'average_rating':rating.average
                	}
	
		return jsonify({'ratings': show_rating})

	except:
		return "Address Id Not Found"


# Update a rating
@ratingController.route('/ratings', methods=['PUT'])
def updateRating():
	#get data from json
	try:
		user_id = request.get_json()["user_id"]
		address_id = request.get_json()["address_id"]
		ratings = session.query(Rating).filter(Rating.user_id==user_id).filter(Rating.address_id==address_id).all()
	except:
		return "User Id and Address Id are necessary"

	cost_rating = request.get_json()["cost_rating"]
	food_rating = request.get_json()["food_rating"]
	cleanliness_rating = request.get_json()["cleanliness_rating"]
	service_rating = request.get_json()["service_rating"]

	total_score = 0
	count = 0

	datetimes = []
	for rating in ratings:
		datetimes.append(rating.date)

	if len(datetimes) > 0:
		latest = max(datetimes)
		difference =  (datetime.utcnow() - latest).days

	
	if difference > 30 :
		try:
			for rating in ratings:
			
				rating.cost_rating = cost_rating	
				rating.food_rating = food_rating	
				rating.cleanliness_rating = cleanliness_rating
				rating.service_rating = service_rating

				new_total_score	 = (rating.cost_rating + rating.service_rating + rating.cleanliness_rating + rating.food_rating)/4

				rating.total_score = new_total_score
				rating.date = datetime.datetime.utcnow()

			session.commit()
			return "Rating Updated"

		except:
			session.rollback()
			return "Rating not Found"		
	else:
		return "User cannot give Rating to this location until %s days" % (30-difference)