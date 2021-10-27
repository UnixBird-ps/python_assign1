from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager



app_title = 'The Watchlist'
DB_NAME = 'database.db'

# Init db instance
db = SQLAlchemy()



def create_app():
	"""
	Sets up Flask app instance
	Sets up sqlite database
	Sets up Flask blueprints
	"""

	from .views import views
	from .auth import auth
	from .models import User, Movie

	# Set up Flask app instance
	app = Flask( __name__ )
	# Create a secret key that prevents cookie manipulation
	app.config[ 'SECRET_KEY' ] = 'testch03taau3df8rgwhh6jghtest'
	# Set up a database URI with protocol and filename
	app.config[ 'SQLALCHEMY_DATABASE_URI' ] = f'sqlite:///{ DB_NAME }'
	db.init_app( app )

	# Web functionality is in separate modules
	# Separate pages for logged in users from pages for not logged in users using Flask blueprints
	app.register_blueprint( views, url_prefix = '/' )
	app.register_blueprint( auth, url_prefix = '/' )

	# Make sure the database exists
	create_database( app )

	# Set up login session logic
	login_manager = LoginManager()
	login_manager.login_view = 'auth.login_get'
	login_manager.init_app( app )

	@login_manager.user_loader
	def load_user( user_id ) :
		return User.query.get( int( user_id ) )

	return app



def create_database( app ) :
	"""
	Checks if the file containing the database is present
	Creates the database file if not
	:param app: Flask app
	:return: Nothing
	"""
	if not path.exists( 'website/' + DB_NAME ) :
		db.create_all( app = app )
		print( 'Created database!' )
