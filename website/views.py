from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Movie
from . import db
import json

views = Blueprint( 'views', __name__ )


#@app.get( '/' )
#def index():
#	return render_template( 'home.html' )


@views.route( "/", methods = [ 'GET', 'POST' ] )
@login_required
def home():
	if request.method == 'POST' :
		movie_title = request.form.get( 'movie_title' )
		movie_genre = request.form.get( 'movie_genre' )
		movie_length = request.form.get( 'movie_length' )
		movie_done = request.form.get( 'done_check' )
		if len( movie_title ) < 1 :
			flash( 'Title is too short!', category = 'error' )
		else :
			new_movie = Movie( title = movie_title, genre = movie_genre, length = movie_length, done = movie_done, user_id = current_user.id )
			db.session.add( new_movie )
			db.session.commit()
			flash( 'Movie added!', category = 'success' )

	return render_template( 'home.html', user = current_user )



@views.route( '/delete-movie', methods = [ 'POST' ] )
def delete_movie() :
	req_movie = json.loads( request.data )
	movie_id = req_movie[ 'id' ]
	movie = Movie.query.get( movie_id )
	if movie :
		if movie.user_id == current_user.id :
			db.session.delete( movie )
			db.session.commit()

	return jsonify( {} )



@views.route( '/done-movie', methods = [ 'POST' ] )
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
