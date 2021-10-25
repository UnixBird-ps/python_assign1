from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Movie
from . import db
import json

views = Blueprint( 'views', __name__ )
app_title = 'The Watchlist'




#@views.route( "/", methods = [ 'GET', 'POST' ] )
@views.post( '/' )
@login_required
def home_post():
	#if request.method == 'POST' :
	form_title = request.form.get( 'movie_title' )
	form_img_url = request.form.get( 'movie_img' )
	form_genre = request.form.get( 'movie_genre' )
	form_length = request.form.get( 'movie_length' )
	if len( form_title ) < 1 :
		flash( 'Title is too short!', category = 'error' )
	else :
		new_movie = Movie( title = form_title, img_src = form_img_url, genre = form_genre, length = form_length, user_id = current_user.id )
		db.session.add( new_movie )
		db.session.commit()
		flash( 'Movie added!', category = 'success' )
	home_get()
	#return render_template( 'home.html', user = current_user, app_title = app_title )




@views.get( '/' )
@login_required
def home_get() :
	return render_template( 'home.html', user = current_user, app_title = app_title )




#@views.route( '/delete-movie', methods = [ 'POST' ] )
@views.post( '/delete-movie' )
@login_required
def delete_movie() :
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	movie = Movie.query.get( movie_id )
	if movie :
		if movie.user_id == current_user.id :
			db.session.delete( movie )
			db.session.commit()
	# Must return something
	return jsonify( {} )




#@views.route( '/done-movie', methods = [ 'POST' ] )
@views.post( '/done-movie' )
@login_required
def done_movie() :
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	movie_done = req_movie[ 'done' ]
	movie = Movie.query.get( movie_id )
	if movie and movie.user_id == current_user.id:
		movie.done = movie_done
		db.session.commit()
	# Must return something
	return jsonify( { } )




#@views.route( '/update-movie-title', methods = [ 'POST' ] )
@views.post( '/update-movie-title' )
@login_required
def update_movie_title() :
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	movie_title = req_movie[ 'title' ]
	movie = Movie.query.get( movie_id )
	if movie and movie.user_id == current_user.id:
		movie.title = movie_title
		print( str( movie.id ) + str( movie.title ) )
		db.session.commit()
	# Must return something
	return jsonify( { } )




#@views.route( '/update-movie-genre', methods = [ 'POST' ] )
@views.post( '/update-movie-genre' )
@login_required
def update_movie_genre() :
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	movie_genre = req_movie[ 'genre' ]
	movie = Movie.query.get( movie_id )
	if movie and movie.user_id == current_user.id:
		movie.genre = movie_genre
		print( str( movie.id ) + str( movie.genre ) )
		db.session.commit()
	# Must return something
	return jsonify( { } )




#@views.route( '/update-movie-length', methods = [ 'POST' ] )
@views.post( '/update-movie-length' )
@login_required
def update_movie_length() :
	"""
	:return: Empty JSON
	"""
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	movie_length = req_movie[ 'length' ]
	movie = Movie.query.get( movie_id )
	if movie and movie.user_id == current_user.id:
		movie.length = movie_length
		print( str( movie.id ) + str( movie.length ) )
		db.session.commit()
	# Must return something
	return jsonify( { } )
