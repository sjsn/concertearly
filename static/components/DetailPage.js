import React from 'react';

import $ from 'jquery';

var DetailPage = React.createClass({
	getInitialState: function() {
		return {data: []}
	},
	componentDidMount: function() {
		$.ajax({
			url: '/api/gen_playlist',
			type: 'POST',
			data: {
				artists: this.props.artists
			},
			success: function(data) {
				console.log(data);
				this.setState({data: data});
				this.handleDetails();
			}.bind(this),
			error: function(xhr, status, err) {
				console.log(xhr);
			}
		});
	},
	handleDetails: function() {
		var details = this.data.map(function(artist) {
			var tracks = this.artist.tracks.map(function(track) {
				return (
					<li key={track.id}><a href={track.url}>{track.name}</a></li>
				);
			});
			return (
				<div>
					<ul className="artist" key={artist.id}>
						<li><h3 className='name'>{artist.name}</h3></li>
						{tracks}
					</ul>
				</div>
			);
		}.bind(this));
		this.setState({details: details})
	},
	render: function() {
		return (
			<div className='details'>
				<h1 className="event">{this.props.date} – {this.props.venue}</h1>
				{this.state.details}
			</div>
		);
	}
});

export default DetailPage;
