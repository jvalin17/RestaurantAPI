# RestaurantAPI


#### Technical Details: 

Language: Python 2.7 
Framework: Flask 
Database: SQLAlchemy, SQLite3 

#### Program Structure: 
Models – Classes for data storage is defined. 
Controllers- processes GET, PUT, POST, DELETE requests from/to ORM based database. 

#### Assumptions: 
You have python and pip installed in your system.  

#### Instructions:
1.	Clone project from git.
2.	Go to Tesla directory through terminal. 
3.	Run the command “pip install requirements.txt”.
4.	Run models.py using command “python models.py”.It sets up database and tables.
5.	Run app.py using command “python app.py”.
6.	Go to Postman App or in browser.
7.	Select your type of request (POST, GET, PUT, DELETE) and give the corresponding url and JSON format Input.

#### API URL and Request formats

1.	Create a user - A user is created
    Request Type: POST
    Url: http://127.0.0.1:5002/users

    Example JSON
    '
    {
            "first_name": "Jim",
            "last_name": "Wobb",
            "phone": 8889901123
    }
    '

2.	Update a user- A user can be updated or deleted
Request Type: PUT
Url- http://127.0.0.1:5002/users/4 (ends with user Id)

Example JSON:
{
            "first_name": "Tyler",
            "last_name": "Wong",
            "phone": 8889901677
}

Request Type: DELETE
Url - http://127.0.0.1:5002/users/4 (ends with user Id)

3.	Get user(s) info - Get all Users
Request Type: GET
Url- http://127.0.0.1:5002/users

4.	Get a single user by User Id
Request Type: GET
Url- http://127.0.0.1:5002/users/3 (ends with user Id)

5.	Create a restaurant - A restaurant is created
Request Type: POST
Url  - http://127.0.0.1:5002/restaurants

Example JSON:
{
            
            "category": "Mexican",
            "city": "Arlington",
            "ratings": 3,
            "name": "Chipotle",
            "state": "TX",
            "street": "254 Cooper St.",
            "zipcode": 75010
 	}

6.	Update a restaurant - A restaurant is updated
Url - http://127.0.0.1:5002/restaurants/2 (ends with address Id)

Request Type: PUT
Example JSON:
{
            
            "category": "Chinese",
            "city": "Houston",
            "state": "TX",
            "street": "112 Lamar Blvd.",
            "zipcode": 72709
}

7.	Get restaurant(s) by name / city/ category/total scoreQuery restaurants with possible filters by restaurant name, city, category or total score.Example: Find Mexican restaurant(s) in San Jose (or zip code) with total score above 3 stars

Request Type: GET
To get all restaurants
Url- http://127.0.0.1:5002/restaurants

Request Type: GET
To get restaurants based on restaurant category/location/Rating, you can modify below url based on your requirement. The results will only be shown for restaurants that have at least 1 rating.
Url- http://127.0.0.1:5002/restaurants?category=Italian&city=Austin

8.	Create a rating for a restaurant by a user - A rating is created for a restaurant by a user
Request Type: POST
Url – http://127.0.0.1:5002/restaurants 
Example JSON
{
            
            "category": "Mexican",
            "city": "Philadelphia",
            "ratings": 3,
            "name": "Chipotle",
            "state": "PA",
            "street": "110 Lambard St.",
            "zipcode": 19107
 	}
 
9.	Update a rating for a restaurant by a user - A rating is updated by a particular user if s/he has given rating before 30 days to that particular restaurant.
Request Type: PUT
Url – http://127.0.0.1:5002/ratings 
Example JSON
{
  	"user_id": 2,
  	"address_id": 2,
  	"cost_rating": 1,
  	"food_rating": 1,
  	"cleanliness_rating": 1,
  	"service_rating": 1
}

10.	Get rating(s) by user - Get a rating or a list of rating given by a user (include all restaurants)
Request Type: GET
Url- http://127.0.0.1:5002/ratings/user=2 (ends with user Id)

11.	Get rating(s) by restaurant(s) - Get a rating or a list of rating by restaurant. All users who gave the scores to the restaurant(s) will be aggregated to total score.
Request Type: GET
Url- http://127.0.0.1:5002/ratings/address=2 (ends with address Id)
