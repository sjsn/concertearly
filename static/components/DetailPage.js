import React from 'react';

import Artist from './Artist';
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
		this.setState({artists: []})
		var details = this.state.data.map(function(artist) {
			artist.tracks.splice(0, 1);
			var allArtists = this.state.artists;
			allArtists.push(artist);
			this.setState({artists: allArtists});
			return (<Artist
						artist={artist}
						onClick={this.handleArtistToggle}
					/>
			);
		}.bind(this));
		this.setState({details: details})
	},
	handleCreateClick: function() {
		// Create playlist with list of artists from this.state.artists
		console.log(this.state.artists);
	},
	handleArtistToggle: function(artist) {
		// Toggle {artist} state from this.state.artists
		var artists = this.state.artists;
		var index = artists.indexOf(artist);
		if (index >= 0) {
			artists.splice(index, 1);
		} else {
			artists.push(artist);
		}
		this.setState({artists: artists});
		console.log(this.state.artists);
	},
	render: function() {
		return (
			<div className="details">
				<h1 className="heading">{this.props.title}</h1>
				<h2 className="sub-heading">{this.props.date} – {this.props.venue}</h2>
				<div className="detail-top">
					<h2>Featuring</h2>
					<button onClick={this.handleCreateClick}>Create Playlist</button>
				</div>
				{this.state.details}
			</div>
		);
	}
});

export default DetailPage;
