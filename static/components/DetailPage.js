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
				this.setState({data: data});
				this.handleDetails();
			}.bind(this),
			error: function(xhr, status, err) {
				console.log(err);
			}
		});
	},
	handleDetails: function() {
		var details = this.state.data.map(function(artist) {
			var tracks = artist.tracks.map(function(track) {
				return (
					<li key={track.id}><a href={track.sample}>{track.name}</a></li>
				);
			});
			return (
				<div>
					<ul className="artist" key={artist.id}>
						<h3 className='name'>{artist.name}</h3>
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
