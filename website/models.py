from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.ext.orderinglist import ordering_list


class Movie( db.Model ) :
	"""
	Holds movie information and a reference to the user that added this object
	"""
	#__tablename__ = 'movie'
	id = db.Column( db.Integer, primary_key = True )
	img_src = db.Column( db.String( 250 ) )
	title = db.Column( db.String( 100 ) )
	genre = db.Column( db.String( 50 ) )
	length = db.Column( db.Integer ) # minutes
	done = db.Column( db.Boolean )
	#date = db.Column( db.DateTime( timezone = True), default = func.now() )
	position = db.Column( db.Integer )
	#user_id = db.Column( db.Integer, db.ForeignKey( 'user.id' ) )
	user_id = db.Column( db.Integer, db.ForeignKey( 'user.id' ) )



class User( db.Model, UserMixin ) :
	"""
	Holds user account information and a reference to movies associated with that account
	"""
	#__tablename__ = 'user'
	id = db.Column( db.Integer, primary_key = True )
	email = db.Column( db.String( 150 ), unique = True )
	password = db.Column( db.String( 150 ) )
	first_name = db.Column( db.String( 150 ) )
	#movies = db.relationship( 'movie', order_by = 'movie.position', collection_class = ordering_list( 'movie.position' ) )
	movies = db.relationship( 'Movie', order_by = 'Movie.position', collection_class = ordering_list( 'position', count_from=0 ) )
