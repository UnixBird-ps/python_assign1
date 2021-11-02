from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
from .models import Movie, User
from . import db, app_title
import json
from sqlalchemy.sql import func, or_, desc, asc
from time import time_ns



# Create a Flask blueprint, attach this module to it
views = Blueprint( 'views', __name__ )



@views.post( '/' )
@login_required
def home_post() :
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
		current_user.movies.append( new_movie )
		#current_user.movies.reorder()
		db.session.commit()
		flash( 'Movie was added!', category = 'success' )
	# Show the home page
	return home_get()



@views.get( '/' )
@login_required
def home_get() :
	"""
	Shows the home page
	:return: The home HTML page using a Flask template
	"""
	#
	#current_user.movies.reorder()
	#db.session.commit()

	# Init a user's session variables that is used to sort or search movies
	if not 'sort_key' in session : session[ 'sort_key'    ] = ''
	if not 'search_term' in session : session[ 'search_term' ] = ''

	# Populate
	search_result = Movie.query.filter( Movie.user_id == current_user.id ).order_by( Movie.position )

	print( current_user )
	sep = ''
	for m in current_user.movies : print( f'{sep}(p:{m.position} t:{m.title} i:{m.id})', end='' ); sep = ', '
	print( '' )

	return render_template( 'home.html', app_title = app_title, user = current_user, search_result = search_result, sort_key = session[ 'sort_key' ], time = time_ns()  )



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
			#db.session.delete( movie )
			current_user.movies.remove( movie )
			current_user.movies.reorder()
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
		# Register the change in the database
		db.session.commit()
	# Must return something
	return jsonify( { } )



@views.post( '/update-movie-length' )
@login_required
def update_movie_length() :
	"""
	Updates the length for a movie with a matching id
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



@views.get( '/search' )
@login_required
def search_get() :
	"""
	This is used for searching movies on title or genre
	:return: HTML list elements containing the movies
	"""
	print( session[ 'sort_key' ] )

	search_result = []
	# Get form data
	search_term = request.args.get( 'q' )
	if search_term :
		session[ 'search_term' ] = search_term
		match session[ 'sort_key' ]:
			case 'title' :
				search_result = Movie.query.filter(
					Movie.user_id == current_user.id,
					or_(
						func.lower( Movie.title ).contains( search_term ),
						func.lower( Movie.genre ).contains( search_term )
					)
				).order_by( Movie.title )
			case 'genre' :
				search_result = Movie.query.filter(
					Movie.user_id == current_user.id,
					or_(
						func.lower( Movie.title ).contains( search_term ),
						func.lower( Movie.genre ).contains( search_term )
					)
				).order_by( Movie.genre )
			case 'length' :
				search_result = Movie.query.filter(
					Movie.user_id == current_user.id,
					or_(
						func.lower( Movie.title ).contains( search_term ),
						func.lower( Movie.genre ).contains( search_term )
					)
				).order_by( Movie.length )
			case _ :
				search_result = Movie.query.filter(
					Movie.user_id == current_user.id,
					or_(
						func.lower( Movie.title ).contains( search_term ),
						func.lower( Movie.genre ).contains( search_term )
					)
				).order_by( Movie.position )
	else :
		match session[ 'sort_key' ]:
			case 'title' :
				search_result = Movie.query.filter( Movie.user_id == current_user.id ).order_by( Movie.title )
			case 'genre' :
				search_result = Movie.query.filter( Movie.user_id == current_user.id ).order_by( Movie.genre )
			case 'length' :
				search_result = Movie.query.filter( Movie.user_id == current_user.id ).order_by( Movie.length )
			case _ :
				search_result = Movie.query.filter( Movie.user_id == current_user.id ).order_by( Movie.position )
	return render_template( 'movies.html', search_result = search_result, query = search_term, sort_key = session[ 'sort_key' ] )



@views.post( '/arrange' )
@login_required
def arrange_post() :
	"""
	Reads JSON data that was sent
	"""
	json_data = json.loads( request.data )
	movie_placement = json_data.get( 'placement' )
	alts = [ 'first', 'up', 'down', 'last' ]
	if movie_placement in alts :
		movie_id = json_data.get( 'id' )
		qm = Movie.query.get( movie_id )
		print( f'p:{qm.position} t:{qm.title} i:{qm.id}' )
		print( f'where: {movie_placement}' )
		movie = current_user.movies.pop( qm.position )
		new_position = qm.position
		match movie_placement :
			case 'first' :
				current_user.movies.insert( 0, movie )
			case 'up' :
				new_position -= 1
				if new_position <= 0 : new_position = 0
				current_user.movies.insert( new_position, movie )
			case 'down' :
				new_position += 1
				current_user.movies.insert( new_position, movie )
			case 'last' :
				current_user.movies.append( movie )
			#case _ :
				#print( 'Not allowed!' )
		current_user.movies.reorder()
		db.session.commit()
	return render_template( 'movies.html', search_result = current_user.movies )



@views.get( '/sort' )
@login_required
def sort_get() :
	"""
	Used for sorting
	Takes a query parameter that is used as a sort key
	:return: A key-sorted list of HTML LI elements containing the movies
	"""
	# Save current sort key
	old_key = session[ 'sort_key' ]
	# Get form data
	received_key = request.args.get( 'key' )
	print( f'old key: {old_key},  received key: {received_key}' )

	if received_key : new_key = received_key
	else : new_key = ''

	match new_key :
		case 'title' :
			if old_key == 'title' : new_key = 'title_reverse'
			if old_key == 'title_reverse' : new_key = 'title'
		case 'genre' :
			if old_key == 'genre' : new_key = 'genre_reverse'
			if old_key == 'genre_reverse' : new_key = 'genre'
		case 'length' :
			if old_key == 'length' : new_key = 'length_reverse'
			if old_key == 'length_reverse' : new_key = 'length'

	current_key = new_key

	print( f'current key: {current_key},  old key: {old_key}' )

	# Set session variable sort_key which is used to sort the list
	session[ 'sort_key' ] = current_key

	search_result = []
	match current_key :
		case 'title' :
			search_result = Movie.query.filter( Movie.user_id == current_user.id ).order_by( Movie.title )
		case 'title_reverse' :
			search_result = Movie.query.filter( Movie.user_id == current_user.id ).order_by( desc( Movie.title ) )
		case 'genre' :
			search_result = Movie.query.filter( Movie.user_id == current_user.id ).order_by( Movie.genre )
		case 'genre_reverse' :
			search_result = Movie.query.filter( Movie.user_id == current_user.id ).order_by( desc( Movie.genre ) )
		case 'length' :
			search_result = Movie.query.filter( Movie.user_id == current_user.id ).order_by( Movie.length )
		case 'length_reverse' :
			search_result = Movie.query.filter( Movie.user_id == current_user.id ).order_by( desc( Movie.length ) )
		case _ :
			search_result = Movie.query.filter( Movie.user_id == current_user.id ).order_by( Movie.position )
	return render_template( 'movies.html', search_result = search_result, query = current_key )



@views.get( '/ui/sort-buttons' )
@login_required
def sortbtns_get() :
	"""
	Used for UI
	:return: HTML code describing the sort buttons
	"""
	print( session[ 'sort_key' ] )
	return render_template( 'sortbtns.html', sort_key = session[ 'sort_key' ] )
