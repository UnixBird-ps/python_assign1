
window.onload = function()
{
	reqMoviesAsHtmlListItems();
}



/**
Deletes a movie on the server
Sends a JSON containing that movie's id
Updates the list in the browser
*/
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



/**
Marks a movie as watched on the server
Sends a JSON containing that movie's id and the state of the checkbox to server
*/
function doneMovie( pMovieId )
{
	var lList = document.getElementById( 'movies' );
	var lListItem = lList.querySelector( 'li#li_' + pMovieId );
	var lCheckBox = lListItem.querySelector( 'input[id^="checkbox_"' );
	fetch( '/done-movie',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId, done : lCheckBox.checked } )
		}
	).then( ( _res ) => {} );
}



/**
Updates the title of a movie on the server
Checks if the value in the input box was changed
Sends a JSON containing that movie's id and the updated title to server
*/
function updateTitle( pMovieId, pInputBox )
{
	if ( pInputBox.value != pInputBox.dataset.lastvalue )
	{
		pInputBox.dataset.lastvalue = pInputBox.value;
		console.log( 'Title differs' );

		fetch( '/update-movie-title',
			{
				method : 'POST',
				body : JSON.stringify( { id : pMovieId, title : pInputBox.value } )
			}
		).then( ( _res ) =>
			{
				console.log( 'Title was updated' );
			}
		);
	}
}



/**
Updates the genre of a movie on the server
Checks if the value in the input box was changed
Sends a JSON containing that movie's id and the updated genre to server
*/
function updateGenre( pMovieId, pInputBox )
{
	if ( pInputBox.value != pInputBox.dataset.lastvalue )
	{
		pInputBox.dataset.lastvalue = pInputBox.value;
		console.log( 'Genre differs' );

		fetch( '/update-movie-genre',
			{
				method : 'POST',
				body : JSON.stringify( { id : pMovieId, genre : pInputBox.value } )
			}
		).then( ( _res ) =>
			{
				console.log( 'Genre was updated' );
			}
		);
	}
}



/**
Updates the length of a movie on the server
Checks if the value in the input box was changed
Sends a JSON containing that movie's id and the updated length to the server
*/
function updateLength( pMovieId, pInputBox )
{
	if ( pInputBox.value != pInputBox.dataset.lastvalue )
	{
		pInputBox.dataset.lastvalue = pInputBox.value;
		console.log( 'Length differs' );

		fetch( '/update-movie-length',
			{
				method : 'POST',
				body : JSON.stringify( { id : pMovieId, length : pInputBox.value } )
			}
		).then( ( _res ) =>
			{
				console.log( 'Length was updated' );
			}
		);
	}
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



/**

*/
function updateModalPoster( pMovieId, pImg )
{
	document.getElementById( 'big_poster_img' ).src = pImg.src;
	var lInputBox = document.getElementById( 'poster_src' );
	lInputBox.value = pImg.src;
	lInputBox.dataset.lastvalue = lInputBox.value;
	document.getElementById( 'submit_poster_url' ).outerHTML = `<button id="submit_poster_url" class="btn btn-primary" data-bs-dismiss="modal" aria-label="Update poster" value="Update" onclick="updateMoviePoster( ${pMovieId} )">Update</button>`;
}



/**

*/
function updateBigPosterUrl( pInputBox )
{
	if ( pInputBox.value != pInputBox.dataset.lastvalue )
	{
		pInputBox.dataset.lastvalue = pInputBox.value;
		console.log( 'Poster URL differs' );

		document.getElementById( 'big_poster_img' ).src = pInputBox.value
	}
}



/**

*/
function updateMoviePoster( pMovieId, pUrl )
{
	var lInputBox = document.getElementById( 'poster_src' );
	fetch( '/update-poster',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId, poster_url : lInputBox.value } )
		}
	).then(
		( _res ) =>
		{
			console.log( 'Poster URL was updated' );
			var lPosterIcon = document.getElementById( 'poster_icon_' + pMovieId );
			lPosterIcon.src = lInputBox.value;
		}
	);
}



/**
*/
function reqMoviesAsHtmlListItems( pQ )
{
	var lReqStr = '/search';

	if ( pQ && pQ.toString().length > 0 ) lReqStr += '?q=' + pQ
	else document.getElementById( 'search_term' ).value = "";

	fetch( lReqStr
	).then(
		_res =>
		{
			_res.text()
			.then( text =>
				{
					var lListElement = document.getElementById( 'movies' );
					lListElement.innerHTML = text;
				}
			);
		}
	);
}



/**
*/
function handleSearchReset( pInputBox )
{
	//console.log( 'handleSearchReset(... : Search input box differs' );
	//console.log( 'handleSearchReset(...', pInputBox.value, pInputBox.value.length );

	if ( pInputBox.value != pInputBox.dataset.lastvalue )
	{
		if ( pInputBox.dataset.lastvalue.length > 0 && ! pInputBox.value.length > 0 ) reqMoviesAsHtmlListItems();
		pInputBox.dataset.lastvalue = pInputBox.value;
	}
}



/**
*/
function handleSearchChange( pInputBox )
{
	console.log( 'handleSearchChange(... : Search input box differs' );
	console.log( 'handleSearchChange(...', pInputBox.value, pInputBox.value.length );
	//if ( ! pInputBox.value.length > 0 ) location.replace( '/' );
}



/**

*/
function moveFirst( pMovieId, pListIndex )
{
	console.log( 'moveFirst', pMovieId, pListIndex );
}



/**

*/
function moveUp( pMovieId, pListIndex )
{
	console.log( 'moveUp', pMovieId, pListIndex );
}



/**

*/
function moveDown( pMovieId, pListIndex )
{
	console.log( 'moveDown', pMovieId, pListIndex );
}



/**

*/
function moveLast( pMovieId, pListIndex )
{
	console.log( 'moveLast', pMovieId, pListIndex );
}
