from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint( 'auth', __name__ )


#@auth.route( '/login', methods = [ 'GET', 'POST' ] )
@auth.post( '/login' )
def login_post() :
	#if request.method == 'POST' :
	form_email = request.form.get( 'email' )
	form_password = request.form.get( 'password' )
	user = User.query.filter_by( email = form_email ).first()
	if user :
		if check_password_hash( user.password, form_password ) :
			flash( 'Logged in successfully!', category = 'success' )
			login_user( user, remember = True )
			return redirect( url_for( 'views.home_get' ) )
		else :
			flash( 'Incorrect password!', category = 'error' )
	else :
		flash( 'Email does not exist.', category = 'error' )
	return  render_template( 'login.html', user = current_user )



@auth.get( '/login' )
def login_get() :
	return  render_template( 'login.html', user = current_user )




#@auth.route( '/signup', methods=[ 'GET', 'POST' ] )
@auth.post( '/signup' )
def signup_post():
	#if request.method == 'POST' :
	form_email = request.form.get( 'email' )
	form_first_name = request.form.get( 'firstname' )
	form_password1 = request.form.get( 'password1' )
	form_password2 = request.form.get( 'password2' )

	user = User.query.filter_by( email = form_email ).first()
	if user :
		flash( 'Email already exists.', category = 'error' )
	elif len( form_email ) < 4 :
		flash( 'Email must be greater than 3 characters.', category = 'error' )
	elif len( form_first_name ) < 2 :
		flash( 'First name must be greater than 1 character.', category = 'error' )
	elif form_password1 != form_password2 :
		flash( 'Passwords don\'t match.', category = 'error' )
	elif len( form_password1 ) < 7 :
		flash( 'Password must be at least 7 characters.', category = 'error' )
	else :
		new_user = User( email = form_email, first_name = form_first_name, password=generate_password_hash( form_password1, method = 'sha256' ) )
		db.session.add( new_user )
		db.session.commit()
		flash( 'Account created!', category = 'success' )
		return redirect( url_for( 'auth.login_get' ) )




@auth.get( '/signup' )
def signup_get():
	return render_template( 'signup.html', user = current_user )




#@auth.route( '/logout' )
@auth.get( '/logout' )
@login_required
def logout_get() :
	logout_user()
	return redirect( url_for( 'auth.login_get' ) )
