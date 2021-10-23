from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Movie
from . import db
import json

views = Blueprint( 'views', __name__ )
app_title = 'The Watchlist'


#@app.get( '/' )
#def index():
#	return render_template( 'home.html' )


#@views.route( "/", methods = [ 'GET', 'POST' ] )
@views.post( '/' )
@login_required
def home_post():
	#if request.method == 'POST' :
	form_title = request.form.get( 'movie_title' )
	form_img_url = request.form.get( 'movie_img' )
	form_genre = request.form.get( 'movie_genre' )
	form_length = request.form.get( 'movie_length' )
	#form_done = request.form.get( 'done_check' )
	if len( form_title ) < 1 :
		flash( 'Title is too short!', category = 'error' )
	else :
		new_movie = Movie( title = form_title, img_src = form_img_url, genre = form_genre, length = form_length, user_id = current_user.id )
		db.session.add( new_movie )
		db.session.commit()
		flash( 'Movie added!', category = 'success' )
	return render_template( 'home.html', user = current_user, app_title = app_title )




@views.get( '/' )
@login_required
def home_get():
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
	return jsonify( {} )




#@views.route( '/done-movie', methods = [ 'POST' ] )
@views.post( '/done-movie' )
@login_required
def done_movie() :
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	movie_done = req_movie[ 'done' ]
	movie = Movie.query.get( movie_id )
	if movie :
		if movie.user_id == current_user.id :
			print( str( movie.id ) + str( movie.done ) )
			movie.done = movie_done
			db.session.commit()
	return jsonify( { } )
