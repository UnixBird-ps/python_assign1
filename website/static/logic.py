from browser import document, alert


def done_movie( movie_id ) :
	print( f'Marking movie with id: ' + str( movie_id ) + ' done.' )


def delete_movie( movie_id ) :
	print( f'Deleting movie with id: ' + str( movie_id ) + '.' )


table = document.select( '#movies' )[ 0 ]
table_trs = table.select( 'tr[id^="tr_"' )
for tr in table_trs :
	movie_id = int( tr[ 'id' ].removeprefix( 'tr_' ) )
	checkbox = tr.select( 'input[id^="checkbox_"' )[ 0 ]
	#alert( checkbox )
	checkbox.bind( 'click', done_movie( movie_id ) )
	div = tr.select( 'div[id^="div_"' )[ 0 ]
	#alert( div )
	div.bind( 'click', delete_movie( movie_id ) )
