from website import create_app
from logging.config import dictConfig

def main() :
	dictConfig(
		{
			'version': 1,
			'formatters': { 'default': { 'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s' } },
			'handlers':
			{
				'wsgi':
				{
					'class': 'logging.StreamHandler',
					'stream': 'ext://flask.logging.wsgi_errors_stream',
					'formatter': 'default'
				}
			},
			'root': { 'level': 'INFO', 'handlers': [ 'wsgi' ] }
		}
	)

	app = create_app()
	app.run( debug = True, port = 8000 )

if __name__ == '__main__':
	main()
