from website import create_app

# Run only when started as standalone
# This prevents running the code when loading
if __name__ == '__main__':
	# Get an Flask app instance
	app = create_app()
	# Start the app with debug enabled
	app.run( debug = True, port = 8000 )
