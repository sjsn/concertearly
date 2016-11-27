import React from 'react';

var HomeContent = React.createClass({
	render: function() {
		if (this.props.items) {
			var searchResults = this.props.items.map(function(item) {
				var artists = item.Artists.map(function(artist) {
					return (
						<span className='artist'>{artist.Name} |</span>
					);
				});
				console.log(item);
				return (
					<div className='result'>
						<p className='venue'>
							<span className='title'>Venue:</span> 
							{item.Venue.Name}
						</p>
						<p className='loc'>
							<span className='title'>Location:</span> 
							{item.Venue.City}, {item.Venue.State}, {item.Venue.ZipCode}
						</p>
						<p className='artists'>
							<span className='title'>Artists:</span> 
							{artists}
						</p>
					</div>
				);
			});
			return (
				<div className='results'>
					<h2>Showing results for '{this.props.term}'</h2>
					{searchResults}
				</div>
			);
		} else {
			return (
				<div>
					<h2 className='result-title'>Showing results for '{this.props.term}'</h2>
					<p className='loading'><i className='fa-spinner'></i></p>
				</div>
			);
		}
	}
});

export default HomeContent;
