from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Movie( db.Model ) :
	id = db.Column( db.Integer, primary_key = True )
	title = db.Column( db.String( 100 ) )
	genre = db.Column( db.String( 50 ) )
	length = db.Column( db.Integer ) # minutes
	done = db.Column( db.Boolean )
	date = db.Column( db.DateTime( timezone = True), default = func.now() )
	user_id = db.Column( db.Integer, db.ForeignKey( 'user.id' ) )

class User( db.Model, UserMixin ) :
	id = db.Column( db.Integer, primary_key = True )
	email = db.Column( db.String( 150 ), unique = True )
	password = db.Column( db.String( 150 ) )
	first_name = db.Column( db.String( 150 ) )
	movies = db.relationship( 'Movie' )
