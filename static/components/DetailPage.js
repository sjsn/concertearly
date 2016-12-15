import React from 'react';

import Artist from './Artist';
import $ from 'jquery';

var DetailPage = React.createClass({
	getInitialState: function() {
		return {data: [], loading: true, 
			created: <button onClick={this.handleCreateClick}>Create Playlist</button>};
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
		var tracks = [];
		for (var i = 0; i < this.state.artists.length; i++) {
			for (var j = 0; j < this.state.artists[i].tracks.length; j++) {
				tracks.push(this.state.artists[i].tracks[j].uri);
			}
		}
		this.setState({tracks: tracks});
		this.setState({loading: false});
		this.setState({details: details});
	},
	handleCreateClick: function() {
		// Create playlist with list of tracks from this.state.tracks
		this.setState({created: 
			<p className="loading play-created"><i className="fa fa-spinner"></i></p>
		});
		$.ajax({
			url: '/api/create_playlist',
			type: 'POST',
			data: {
				tracks: this.state.tracks,
				playlist_name: this.props.title
			},
			success: function(data) {
				console.log(data);
				if (data.success >= 0) {
					console.log('success!');
					this.setState({created: 
						<p className="play-created"><a href={"http://open.spotify.com/user/spotify/playlist/" + data.id} target="_blank">Playlist Created <i className="fa fa-check-circle created"></i></a></p>
					});
				} else {
					console.log('fail...');
					{this.setState({created: 
						<p className="play-created failed">Failed to make playlist. <button onClick={this.handleCreateClick}>Retry</button></p>
					})}
				}
			}.bind(this),
			error: function(xhr, status, err) {
				console.log(err);
				this.setState({created: 
					<p className="play-created failed">Failed to make playlist. Please make sure you're <a href="/spotify/auth">signed in</a>.</p>
				});
			}
		});
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
		var tracks = [];
		for (var i = 0; i < this.state.artists.length; i++) {
			for (var j = 0; j < this.state.artists[i].tracks.length; j++) {
				tracks.push(this.state.artists[i].tracks[j].uri);
			}
		}
		this.setState({tracks: tracks});
	},
	render: function() {
		if (!this.state.loading) {
			return (
				<div className="details">
					<h1 className="heading">{this.props.title}</h1>
					<h2 className="sub-heading">{this.props.date} – {this.props.venue}</h2>
					<div className="detail-top">
						<h2>Featuring</h2>
						{this.state.created}
					</div>
					{this.state.details}
				</div>
			);
		} else if (this.state.error) {
			return (
				<div className="error">
					<p>There was an error retrieving the information. Please try again later.</p>
				</div>
			);
		} else {
			return (
				<div className="details">
					<p className='loading'><i className='fa fa-spinner'></i></p>
				</div>
			);
		}
	}
});

export default DetailPage;
