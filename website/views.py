from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Movie
from . import db, app_title
import json



# Create a Flask blueprint, attach this module to it
views = Blueprint( 'views', __name__ )



@views.post( '/' )
@login_required
def home_post():
	"""
	Reads form data that was sent from the webpage
	Validates movie title length that was sent in the form
	Registers the movie in the database
	:return: The home page
	"""
	# Get form data
	form_title = request.form.get( 'movie_title' )
	form_img_url = request.form.get( 'movie_img' )
	form_genre = request.form.get( 'movie_genre' )
	form_length = request.form.get( 'movie_length' )
	# See if form data is valid
	if len( form_title ) < 1 :
		flash( 'Title is too short!', category = 'error' )
	else :
		# Attempt was successful
		# Create new movie object
		new_movie = Movie( title = form_title, img_src = form_img_url, genre = form_genre, length = form_length, user_id = current_user.id )
		# Register the movie in the database
		db.session.add( new_movie )
		db.session.commit()
		flash( 'Movie added!', category = 'success' )
	# Show the home page
	return home_get()



@views.get( '/' )
@login_required
def home_get() :
	"""
	Shows the home page
	:return: The home HTML page using a Flask template
	"""
	return render_template( 'home.html', user = current_user, app_title = app_title )



@views.post( '/delete-movie' )
@login_required
def delete_movie() :
	"""
	This function removes the movie with a matching id
	Reads JSON data that was sent
	Updates the database if a movie matching the id in the JSON was found
	:return: Empty JSON
	"""
	# Get JSON data that was sent
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	# Find first movie in the database matching the id
	movie = Movie.query.get( movie_id )
	# Was the movie found?
	if movie :
		if movie.user_id == current_user.id :
			db.session.delete( movie )
			# Register the change in the database
			db.session.commit()
	# Must return something
	return jsonify( {} )



@views.post( '/done-movie' )
@login_required
def done_movie() :
	"""
	Marks the movie with a matching id as watched
	Reads JSON data that was sent
	Updates the database if a movie matching the id in the JSON was found
	:return: Empty JSON
	"""
	# Get JSON data that was sent
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	movie_done = req_movie[ 'done' ]
	# Find first movie in the database matching the id
	movie = Movie.query.get( movie_id )
	# Was the movie found?
	if movie and movie.user_id == current_user.id:
		movie.done = movie_done
		# Register the change in the database
		db.session.commit()
	# Must return something
	return jsonify( { } )



@views.post( '/update-movie-title' )
@login_required
def update_movie_title() :
	"""
	This function updates the title for a movie with a matching id
	Reads JSON data that was sent
	Updates the database if a movie matching the id in the JSON was found
	:return: Empty JSON
	"""
	# Get JSON data that was sent
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	movie_title = req_movie[ 'title' ]
	# Find first movie in the database matching the id
	movie = Movie.query.get( movie_id )
	# Was the movie found?
	if movie and movie.user_id == current_user.id:
		movie.title = movie_title
		print( str( movie.id ) + str( movie.title ) )
		# Register the change in the database
		db.session.commit()
	# Must return something
	return jsonify( { } )



@views.post( '/update-movie-genre' )
@login_required
def update_movie_genre() :
	"""
	This function updates the genre for a movie with a matching id
	Reads JSON data that was sent
	Updates the database if a movie matching the id in the JSON was found
	:return: Empty JSON
	"""
	# Get JSON data that was sent
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	movie_genre = req_movie[ 'genre' ]
	# Find first movie in the database matching the id
	movie = Movie.query.get( movie_id )
	# Was the movie found?
	if movie and movie.user_id == current_user.id:
		movie.genre = movie_genre
		print( str( movie.id ) + str( movie.genre ) )
		# Register the change in the database
		db.session.commit()
	# Must return something
	return jsonify( { } )



@views.post( '/update-movie-length' )
@login_required
def update_movie_length() :
	"""
	This function updates the length for a movie with a matching id
	Reads JSON data that was sent
	Updates the database if a movie matching the id in the JSON was found
	:return: Empty JSON
	"""
	# Get JSON data that was sent
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	movie_length = req_movie[ 'length' ]
	# Find first movie in the database matching the id
	movie = Movie.query.get( movie_id )
	# Was the movie found?
	if movie and movie.user_id == current_user.id:
		movie.length = movie_length
		# Register the change in the database
		db.session.commit()
	# Must return something
	return jsonify( { } )



@views.post( '/update-poster' )
@login_required
def update_movie_poster() :
	"""
	This function updates the poster image url for a movie with a matching id
	Reads JSON data that was sent
	Updates the database if a movie matching the id in the JSON was found
	:return: Empty JSON
	"""
	# Get JSON data that was sent
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	movie_poster_url = req_movie[ 'poster_url' ]
	# Find first movie in the database matching the id
	movie = Movie.query.get( movie_id )
	if movie and movie.user_id == current_user.id:
		movie.img_src = movie_poster_url
		db.session.commit()
	# Must return something
	return jsonify( { } )
