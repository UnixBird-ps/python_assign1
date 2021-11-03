from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
from .models import Movie
from . import db, app_title
import json
from sqlalchemy.sql import func, or_, desc
from time import time_ns



# Create a Flask blueprint, attach this module to it
views = Blueprint( 'views', __name__ )


def get_movies_from_db() :
	"""
	Fetches movies from the database
	Used by other functions in this module
	Creates a sorted and filtered list of movies
	sorted on current session variable sort_key
	filtered on current session variable search_term
	:return: An object of type list
	"""
	search_result = []
	match session[ 'sort_key' ] :
		case 'title' :
			# Get data from db, search in title and genre
			search_result = Movie.query.filter(
				Movie.user_id == current_user.id,
				or_(
					func.lower( Movie.title ).contains( session[ 'search_term' ] ),
					func.lower( Movie.genre ).contains( session[ 'search_term' ] )
				)
			).order_by( Movie.title ) # Sort on title
		case 'title_reverse' :
			# Get data from db, search in title and genre
			search_result = Movie.query.filter(
				Movie.user_id == current_user.id,
				or_(
					func.lower( Movie.title ).contains( session[ 'search_term' ] ),
					func.lower( Movie.genre ).contains( session[ 'search_term' ] )
				)
			).order_by( desc( Movie.title ) ) # Sort on title, reversed
		case 'genre' :
			# Get data from db, search in title and genre
			search_result = Movie.query.filter(
				Movie.user_id == current_user.id,
				or_(
					func.lower( Movie.title ).contains( session[ 'search_term' ] ),
					func.lower( Movie.genre ).contains( session[ 'search_term' ] )
				)
			).order_by( Movie.genre ) # Sort on genre
		case 'genre_reverse' :
			# Get data from db, search in title and genre
			search_result = Movie.query.filter(
				Movie.user_id == current_user.id,
				or_(
					func.lower( Movie.title ).contains( session[ 'search_term' ] ),
					func.lower( Movie.genre ).contains( session[ 'search_term' ] )
				)
			).order_by( desc( Movie.genre ) ) # Sort on genre, reversed
		case 'length' :
			# Get data from db, search in title and genre
			search_result = Movie.query.filter(
				Movie.user_id == current_user.id,
				or_(
					func.lower( Movie.title ).contains( session[ 'search_term' ] ),
					func.lower( Movie.genre ).contains( session[ 'search_term' ] )
				)
			).order_by( Movie.length ) # Sort on length
		case 'length_reverse' :
			# Get data from db, search in title and genre
			search_result = Movie.query.filter(
				Movie.user_id == current_user.id,
				or_(
					func.lower( Movie.title ).contains( session[ 'search_term' ] ),
					func.lower( Movie.genre ).contains( session[ 'search_term' ] )
				)
			).order_by( desc( Movie.length ) ) # Sort on length, reversed
		case _ :
			# Get data from db, search in title and genre, sort on position
			search_result = Movie.query.filter(
				Movie.user_id == current_user.id,
				or_(
					func.lower( Movie.title ).contains( session[ 'search_term' ] ),
					func.lower( Movie.genre ).contains( session[ 'search_term' ] )
				)
			).order_by( Movie.position )
	return search_result


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
		current_user.movies.reorder()
		db.session.commit()
		flash( 'Movie was added!', category = 'success' )
	# Show the home page
	return home_get()



@views.get( '/' )
@login_required
def home_get() :
	"""
	Shows the home page
	Initializes a few session vars
	:return: The home HTML page using a Flask template
	"""
	# Init missing session variables that are used to sort or search movies
	if not 'search_term' in session : session[ 'search_term' ] = ''
	if not 'sort_key' in session : session[ 'sort_key'    ] = ''
	if not 'sortbtn_title_reverse' in session : session[ 'sortbtn_title_reverse' ] = False
	if not 'sortbtn_genre_reverse' in session : session[ 'sortbtn_genre_reverse' ] = False
	if not 'sortbtn_length_reverse' in session : session[ 'sortbtn_length_reverse' ] = False
	# Populate list with movies with default sorting
	search_result = get_movies_from_db()
	# Log some info
	print( f'current_user: [{current_user}]' )
	sep = ''
	for m in current_user.movies : print( f'{sep}(p:{m.position} t:{m.title} i:{m.id})', end='' ); sep = ', '
	print( '' )
	# Return the page
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
	# Must return something, return empty JSON
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
	# Must return something, return empty JSON
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
	# Must return something, return empty JSON
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
	# Must return something, return empty JSON
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
	# Must return something, return empty JSON
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
	# Must return something, return empty JSON
	return jsonify( { } )



@views.get( '/search' )
@login_required
def search_get() :
	"""
	This is used for searching movies on title or genre
	:return: HTML list elements containing the movies
	"""
	# Get form data
	search_term = request.args.get( 'q' )
	if search_term : session[ 'search_term' ] = search_term
	else : session[ 'search_term' ] = ''
	# Log some info
	print( f'session sort_key: [{session[ "sort_key" ]}]' )
	print( f'session search_term: [{session[ "search_term" ]}]' )

	search_result = get_movies_from_db()
	return render_template( 'movies.html', search_result = search_result, query = search_term, sort_key = session[ 'sort_key' ] )



@views.post( '/arrange' )
@login_required
def arrange_post() :
	"""
	Used for rearranging the movies in the list
	Reads JSON data that was sent
	"""
	# Get JSON data that was sent
	json_data = json.loads( request.data )
	movie_id = json_data.get( 'id' )
	movie_placement = json_data.get( 'placement' )
	# Find the movie in db
	qm = Movie.query.get( movie_id )
	# Make sure the placement is valid
	alts = [ 'first', 'up', 'down', 'last' ]
	if qm and movie_placement in alts :
		# Log some info
		print( f'p:{qm.position}  t:{qm.title}  i:{qm.id}  where:[{movie_placement}]' )
		# Remove movie from list
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
			case _ :
				print( 'Not allowed!' )
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
	# Save current session sort key
	old_session_key = session[ 'sort_key' ]
	# Get query vars
	received_key = request.args.get( 'key' )
	# Log some info
	print( f'received key from ui: [{received_key}],  old session key: [{old_session_key}]' )
	# Set the sort key to a sane state
	if not received_key : received_key = ''
	# Reverse the sorting order only if the user requested same sort key a second time in a row
	new_session_key = received_key

	if received_key == 'title' : # Assuming that the user has clicked on the sort button "Title"
		if 'title' in old_session_key : # Same button was clicked twise in a row, change the state
			if session[ 'sortbtn_title_reverse' ] :
				session[ 'sortbtn_title_reverse' ] = False
				new_session_key = 'title'
			else :
				session[ 'sortbtn_title_reverse' ] = True
				new_session_key = 'title_reverse'
		else :                          # Different button was clicked than before, keep same state
			if session[ 'sortbtn_title_reverse' ] :
				new_session_key = 'title_reverse'
			else :
				new_session_key = 'title'

	if received_key == 'genre' :
		if 'genre' in old_session_key : # Same button was clicked twise in a row, change the state
			if session[ 'sortbtn_genre_reverse' ] :
				session[ 'sortbtn_genre_reverse' ] = False
				new_session_key = 'genre'
			else :
				session[ 'sortbtn_genre_reverse' ] = True
				new_session_key = 'genre_reverse'
		else :                          # Different button was clicked than before, keep same state
			if session[ 'sortbtn_genre_reverse' ] :
				new_session_key = 'genre_reverse'
			else :
				new_session_key = 'genre'

	if received_key == 'length' :
		if 'length' in old_session_key : # Same button was clicked twise in a row, change the state
			if session[ 'sortbtn_length_reverse' ] :
				session[ 'sortbtn_length_reverse' ] = False
				new_session_key = 'length'
			else :
				session[ 'sortbtn_length_reverse' ] = True
				new_session_key = 'length_reverse'
		else :                          # Different button was clicked than before, keep same state
			if session[ 'sortbtn_length_reverse' ] :
				new_session_key = 'length_reverse'
			else :
				new_session_key = 'length'

	# Log some info
	print( f'current key: [{new_session_key}]' )
	# Set session variable sort_key which is used to sort the list
	session[ 'sort_key' ] = new_session_key
	search_result = get_movies_from_db()
	# Return the movies page
	return render_template( 'movies.html', search_result = search_result, query = new_session_key, sort_key = new_session_key )



@views.get( '/ui/sort-buttons' )
@login_required
def sortbtns_get() :
	"""
	Used for rendering of sort buttons in GUI
	:return: HTML code describing the sort buttons
	"""
	# Create default button states
	sort_buttons = []
	sort_buttons.append( { 'btn_id' : 'btn_sort_off',    'btn_class' : 'btn-outline-success', 'label': 'Sort:Off', 'sort_key': '',       'reverse' : False } )
	sort_buttons.append( { 'btn_id' : 'btn_sort_title',  'btn_class' : 'btn-outline-success', 'label': 'Title',    'sort_key': 'title',  'reverse' : session[ 'sortbtn_title_reverse' ] } )
	sort_buttons.append( { 'btn_id' : 'btn_sort_genre',  'btn_class' : 'btn-outline-success', 'label': 'Genre',    'sort_key': 'genre',  'reverse' : session[ 'sortbtn_genre_reverse' ] } )
	sort_buttons.append( { 'btn_id' : 'btn_sort_length', 'btn_class' : 'btn-outline-success', 'label': 'Length',   'sort_key': 'length', 'reverse' : session[ 'sortbtn_length_reverse' ] } )

	# Modify states of the sort buttons depending on the current session var sort_key
	# This changes the jinja variable used for rendering the html page for sort buttons
	match session[ 'sort_key' ].removesuffix( '_reverse' ) :
		case '' : sort_buttons[ 0 ][ 'btn_class' ] = 'btn-success'
		case 'title' : sort_buttons[ 1 ][ 'btn_class' ] = 'btn-success'
		case 'genre' : sort_buttons[ 2 ][ 'btn_class' ] = 'btn-success'
		case 'length' : sort_buttons[ 3 ][ 'btn_class' ] = 'btn-success'

	# Return the buttons page
	return render_template( 'sortbtns.html', sort_key = session[ 'sort_key' ], sort_buttons = sort_buttons, time = time_ns() )
