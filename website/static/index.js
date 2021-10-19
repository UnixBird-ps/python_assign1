
function deleteMovie( pMovieId )
{
	fetch( '/delete-movie',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId } )
		}
	).then(
		( _res ) =>
		{
			var lTable = document.getElementById( 'movies' );
			var lTableRow = lTable.querySelector( 'tr#tr_' + pMovieId );
			lTableRow.remove();
			tableChanged();
		}
	);
}


function doneMovie( pMovieId )
{
	var lTable = document.getElementById( 'movies' );
	var lRow = lTable.querySelector( 'tr#tr_' + pMovieId );
	var lCheckBox = lRow.querySelector ( 'input[type="checkbox"]' );
	fetch( '/done-movie',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId, done : lCheckBox.checked } )
		}
	).then( ( _res ) => {} );
}

function tableChanged()
{
	var lTable = document.getElementById( 'movies' );
	var lRows = lTable.querySelectorAll( 'tr[id^="tr_"' );
	var lRowNum = 0;
	for ( let lRow of lRows )
	{
		lRowNum++;
		var lNumCell = lRow.querySelector ( 'th' );
		lNumCell.innerHTML = lRowNum;
	}
}
