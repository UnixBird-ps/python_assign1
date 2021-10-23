
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
			renumTableRows();
		}
	);
}



function doneMovie( pMovieId )
{
	var lTable = document.getElementById( 'movies' );
	var lTableRow = lTable.querySelector( 'tr#tr_' + pMovieId );
	var lCheckBox = lTableRow.querySelector ( 'input[id^="checkbox_"' );
	fetch( '/done-movie',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId, done : lCheckBox.checked } )
		}
	).then( ( _res ) => {} );
}



function renumTableRows()
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



function updateModalPoster( pButton )
{
	var lImage = pButton.querySelector( 'img' );
	document.getElementById( 'big-poster' ).src = lImage.src;
}