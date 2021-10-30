

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
	var lCheckBox = lListItem.querySelector( 'input[id^="checkbox_"' );
	fetch( '/done-movie',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId, done : lCheckBox.checked } )
		}
	).then( ( _res ) => {} );
}



function updateTitle( pMovieId, pInputBox )
{
	if ( pInputBox.value != pInputBox.dataset.lastvalue )
	{
		pInputBox.dataset.lastvalue = pInputBox.value;
		console.log( 'Title changed' );

		fetch( '/update-movie-title',
			{
				method : 'POST',
				body : JSON.stringify( { id : pMovieId, title : pInputBox.value } )
			}
		).then( ( _res ) => {} );
	}
}



function updateGenre( pMovieId, pInputBox )
{
	if ( pInputBox.value != pInputBox.dataset.lastvalue )
	{
		pInputBox.dataset.lastvalue = pInputBox.value;
		console.log( 'Genre changed' );

		fetch( '/update-movie-genre',
			{
				method : 'POST',
				body : JSON.stringify( { id : pMovieId, genre : pInputBox.value } )
			}
		).then( ( _res ) => {} );
	}
}



function updateLength( pMovieId, pInputBox )
{
	if ( pInputBox.value != pInputBox.dataset.lastvalue )
	{
		pInputBox.dataset.lastvalue = pInputBox.value;
		console.log( 'Length changed' );

		fetch( '/update-movie-length',
			{
				method : 'POST',
				body : JSON.stringify( { id : pMovieId, length : pInputBox.value } )
			}
		).then( ( _res ) => {} );
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
		console.log( 'Poster URL has changed' );

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
			var lPosterIcon = document.getElementById( 'poster_icon_' + pMovieId );
			lPosterIcon.src = lInputBox.value;
		}
	);
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
