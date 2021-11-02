
window.onload = function()
{
	// Populate movies list
	reqMoviesAsHtmlListItems();

	var pE = document.getElementById( 'navbar-container' );
	//var pTitle = document.getElementById( 'app-title' );

	if ( pE && document.body )
	{
		document.body.style.paddingTop = pE.offsetHeight + 'px';

		window.onresize = function()
		{
			document.body.style.paddingTop = pE.offsetHeight + 'px';
		};
	}

	// Link the submit button's click handler to Enter keyup event of the search input box
	// Get the input field
	var lInputBox = document.getElementById( 'search_term' );
	if ( lInputBox )
	{
		// Execute a function when the user releases a key on the keyboard
		lInputBox.addEventListener( 'keyup',
			event =>
			{
				// Number 13 is the "Enter" key on the keyboard
				if ( event.key === 'Enter' )
				{
					// Cancel the default action, if needed
					event.preventDefault();
					// Trigger the button element with a click
					document.getElementById( 'search_submit' ).click();
				}
			}
		);
	}
}



function constructAlert( pMsg, pCat )
{
	var lMsgHTML = '<div class="alert ' + pCat + ' alert-dismissible fade show my-0" role="alert">';
	lMsgHTML += '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>';
	lMsgHTML += '<span>' + pMsg + '</span>';
	lMsgHTML += '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
	lMsgHTML += '</div>';
	return lMsgHTML;
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
		_res => { reqMoviesAsHtmlListItems(); }
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
	).then(
		_res => {}
	);
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

		fetch( '/update-movie-title',
			{
				method : 'POST',
				body : JSON.stringify( { id : pMovieId, title : pInputBox.value } )
			}
		).then(
			_res =>
			{
				var lMsgContainer = document.getElementById( 'message-container' );
				lMsgContainer.innerHTML += constructAlert( 'Title was updated', 'alert-success' );
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

		fetch( '/update-movie-genre',
			{
				method : 'POST',
				body : JSON.stringify( { id : pMovieId, genre : pInputBox.value } )
			}
		).then(
			_res =>
			{
				var lMsgContainer = document.getElementById( 'message-container' );
				lMsgContainer.innerHTML += constructAlert( 'Genre was updated', 'alert-success' );
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

		fetch( '/update-movie-length',
			{
				method : 'POST',
				body : JSON.stringify( { id : pMovieId, length : pInputBox.value } )
			}
		).then(
			_res =>
			{
				var lMsgContainer = document.getElementById( 'message-container' );
				lMsgContainer.innerHTML += constructAlert( 'Length was updated', 'alert-success' );
			}
		);
	}
}



function updateModalPoster( pMovieId, pImg )
{
	document.getElementById( 'big_poster_img' ).src = pImg.src;
	var lInputBox = document.getElementById( 'poster_src' );
	lInputBox.value = pImg.src;
	lInputBox.dataset.lastvalue = lInputBox.value;
	document.getElementById( 'submit_poster_url' ).outerHTML = `<button id="submit_poster_url" class="btn btn-primary" data-bs-dismiss="modal" aria-label="Update poster" value="Update" onclick="updateMoviePoster( ${pMovieId} )">Update</button>`;
}



function updateBigPosterUrl( pInputBox )
{
	if ( pInputBox.value != pInputBox.dataset.lastvalue )
	{
		pInputBox.dataset.lastvalue = pInputBox.value;
		console.log( 'Poster URL differs' );

		document.getElementById( 'big_poster_img' ).src = pInputBox.value;
	}
}



function updateMoviePoster( pMovieId, pUrl )
{
	var lInputBox = document.getElementById( 'poster_src' );
	fetch( '/update-poster',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId, poster_url : lInputBox.value } )
		}
	).then(
		_res =>
		{
			var lPosterIcon = document.getElementById( 'poster_icon_' + pMovieId );
			lPosterIcon.src = lInputBox.value;

			var lMsgContainer = document.getElementById( 'message-container' );
			lMsgContainer.innerHTML += constructAlert( 'Poster was updated', 'alert-success' );
		}
	);
}



function reqMoviesAsHtmlListItems( pQ )
{
	if ( document.getElementById( 'movies' ) )
	{
		var lReqStr = '/search';

		if ( pQ && pQ.toString().length > 0 ) { lReqStr += '?q=' + pQ; }
		else { document.getElementById( 'search_term' ).value = ""; }

		fetch( lReqStr )
		.then(
			_res =>
			{
				_res.text()
				.then(
					text =>
					{
						var lListElement = document.getElementById( 'movies' );
						lListElement.innerHTML = text;
					}
				);
			}
		);
	}
}



function handleSearchReset( pInputBox )
{
	if ( pInputBox.value != pInputBox.dataset.lastvalue )
	{
		if ( pInputBox.dataset.lastvalue.length > 0 && ! pInputBox.value.length > 0 ) reqMoviesAsHtmlListItems();
		pInputBox.dataset.lastvalue = pInputBox.value;
	}
}



function arrangeMovie( pMovieId, pListIndex, pPlacement )
{
	fetch( '/arrange',
		{
			method : 'POST',
			body : JSON.stringify( { id : pMovieId, placement : pPlacement } )
		}
	).then(
		_res =>
		{
			_res.text()
			.then(
				text =>
				{
					var lListElement = document.getElementById( 'movies' );
					lListElement.innerHTML = text;
				}
			);
		}
	);
}



function reqSorted( pSortKey )
{
	var lReqStr = '/sort';

	if ( pSortKey && pSortKey.toString().length > 0 ) { lReqStr += '?key=' + pSortKey; }

	fetch( lReqStr )
	.then(
		_res =>
		{
			_res.text()
			.then(
				text =>
				{
					var lListElement = document.getElementById( 'movies' );
					lListElement.innerHTML = text;

					fetch( '/ui/sort-buttons' )
					.then(
						_res =>
						{
							_res.text()
							.then(
								text =>
								{
									var lSortButtons = document.getElementById( 'sort-buttons-container' );
									lSortButtons.innerHTML = text;
								}
							);
						}
					);
				}
			);
		}
	);
}
