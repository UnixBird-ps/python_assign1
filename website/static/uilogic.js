
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
			var lList = document.getElementById( 'movies' );
			var lListItem = lList.querySelector( 'li#li_' + pMovieId );
			lListItem.remove();
			//renumTableRows();
		}
	);
}



function doneMovie( pMovieId )
{
	var lList = document.getElementById( 'movies' );
	var lListItem = lList.querySelector( 'li#li_' + pMovieId );
	var lCheckBox = lListItem.querySelector ( 'input[id^="checkbox_"' );
	fetch( '/done-movie',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId, done : lCheckBox.checked } )
		}
	).then( ( _res ) => {} );
}



function updateTitle( pMovieId, pInputBox )
{
	var lTitleStr = pInputBox.value;
	console.log( pMovieId, lTitleStr );
	fetch( '/update-movie-title',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId, title : lTitleStr } )
		}
	).then( ( _res ) => {} );
}



function updateGenre( pMovieId, pInputBox )
{
	var lGenreStr = pInputBox.value;
	console.log( pMovieId, lGenreStr );
	fetch( '/update-movie-genre',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId, genre : lGenreStr } )
		}
	).then( ( _res ) => {} );
}



function updateLength( pMovieId, pInputBox )
{
	var lLength = pInputBox.value;
	console.log( pMovieId, lLength );
	fetch( '/update-movie-length',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId, length : lLength } )
		}
	).then( ( _res ) => {} );
}



function renumTableRows()
{
	var lList = document.getElementById( 'movies' );
	var lListItems = lList.querySelectorAll( 'li[id^="li_"' );
	var lRowNum = 0;
	for ( let lItem of lListItems )
	{
		lRowNum++;
		var lNumCell = lItem.querySelector ( 'th' );
		lNumCell.innerHTML = lRowNum;
	}
}



function updateModalPoster( pImg )
{
	//var lImage = pButton.querySelector( 'img' );
	//document.getElementById( 'big-poster' ).src = lImage.src;
	document.getElementById( 'big-poster' ).src = pImg.src;
}