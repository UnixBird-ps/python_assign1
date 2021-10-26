from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint( 'auth', __name__ )


@auth.post( '/login' )
def login_post() :
	"""
	Reads form data that was sent from the webpage
	Redirects the user to propper webpage
	:return: If login was successful a HTTP redirect response to the home page, or the login page again
	"""
	# Get form data
	form_email = request.form.get( 'email' )
	form_password = request.form.get( 'password' )
	form_remember_me = request.form.get( 'remember_me' )
	# Translate remember_me checkbox's state to boolean
	if form_remember_me == 'on' : form_remember_me = True
	else : form_remember_me = False
	# Get first user from database matching mail address in the form
	user = User.query.filter_by( email = form_email ).first()
	if user :
		# See if the password from the form matches the password in the database
		if check_password_hash( user.password, form_password ) :
			flash( 'Logged in successfully!', category = 'success' )
			login_user( user, remember = form_remember_me )
			return redirect( url_for( 'views.home_get' ) )
		else :
			flash( 'Incorrect password!', category = 'error' )
	else :
		flash( 'Email does not exist.', category = 'error' )
	login_get()



@auth.get( '/login' )
def login_get() :
	"""
	Shows the login page
	:return: The login page using a Flask template
	"""
	return  render_template( 'login.html', user = current_user )




@auth.post( '/signup' )
def signup_post():
	"""
	Reads form data that was sent from the webpage
	Checks if data was valid
	Registers user in the database
	Redirects the user to propper webpage
	:return: If successful a HTTP redirect response to the login page, or the signup page again
	"""
	# Get form data
	form_email = request.form.get( 'email' )
	form_first_name = request.form.get( 'firstname' )
	form_password1 = request.form.get( 'password1' )
	form_password2 = request.form.get( 'password2' )
	# Find first user in the database matching mail address in the form
	user = User.query.filter_by( email = form_email ).first()
	# See if form data is valid
	if user :
		# Account is already present
		flash( 'Email already exists.', category = 'error' )
	elif len( form_email ) < 5 :
		flash( 'Email must be greater than 3 characters.', category = 'error' )
	elif len( form_first_name ) < 2 :
		flash( 'First name must be greater than 1 character.', category = 'error' )
	elif len( form_password1 ) < 7 :
		flash( 'Password must be at least 7 characters.', category = 'error' )
	elif form_password1 != form_password2 :
		flash( 'Passwords don\'t match.', category = 'error' )
	else :
		# Signup attempt was successful
		# Create the user object
		new_user = User( email = form_email, first_name = form_first_name, password=generate_password_hash( form_password1, method = 'sha256' ) )
		# Register the user in the database
		db.session.add( new_user )
		db.session.commit()
		flash( 'Account created!', category = 'success' )
		# Redirect user to login page
		return redirect( url_for( 'auth.login_get' ) )
	# Call get method again because signup was unsuccessful, let the user retry
	signup_get()




@auth.get( '/signup' )
def signup_get() :
	"""
	Shows the signup page
	:return: The signup page using a Flask template
	"""
	return render_template( 'signup.html', user = current_user )




@auth.get( '/logout' )
@login_required
def logout_get() :
	"""
	Logs out the user
	Redirects the user to login page
	:return: A HTTP redirect response
	"""
	logout_user()
	return redirect( url_for( 'auth.login_get' ) )
