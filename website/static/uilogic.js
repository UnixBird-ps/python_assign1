
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




function updateModalPoster( pMovieId, pImg )
{
	document.getElementById( 'big_poster' ).src = pImg.src;
	document.getElementById( 'poster_src' ).value = pImg.src;
	document.getElementById( 'submit_poster_url' ).outerHTML = `<button id="submit_poster_url" class="btn btn-primary" data-bs-dismiss="modal" aria-label="Update poster" value="Update" onclick="updatePoster( ${pMovieId} )">Update</button>`;
}



function updatePoster( pMovieId )
{
	fetch( '/update-poster',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId, poster_url : document.getElementById( 'poster_src' ).value } )
		}
	).then(
		( _res ) =>
		{
			var lPosterIcon = document.getElementById( 'poster_icon_' + pMovieId );
			lPosterIcon.src = document.getElementById( 'poster_src' ).value;
		}
	);
}
