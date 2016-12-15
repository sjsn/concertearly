import React from 'react';

import Track from './Track';
import Table from 'react-bootstrap/lib/Table';

var Artist = React.createClass({
	getInitialState: function() {
		return {added: true, icon: <i className="fa fa-check-circle-o added-ico"></i>};
	},
	componentWillMount: function() {
		var tracks = this.props.artist.tracks.map(function(track) {
			return (
				<Track track={track} onClick={this.handlePlay} />
			);
		}.bind(this));
		this.setState({tracks: tracks});
	},
	handleToggle: function() {
		this.props.onClick(this.props.artist);
		if (!this.state.added) {
			this.setState({icon: <i className="fa fa-check-circle-o added-ico"></i>});
		} else {
			this.setState({icon: <i className="fa fa-plus-circle add-ico"></i>});
		}
		this.setState({added: !this.state.added});
	},
	handlePlay: function(track) {
		console.log(track);
	},
	render: function() {
		return (
			<div key={this.props.artist.id} className="concert-artist">
				<div className="artist">
					<div className="artist-top">
						<h3 className='name'>{this.props.artist.name}</h3>
						<button className="add-toggle" onClick={this.handleToggle}>
							{this.state.icon}
						</button>
					</div>
					<img src={this.props.artist.image} alt={this.props.artist.name} className="artist-img" />
					<div className="content">
						<p className="track-title">Popular Tracks: </p>
						<Table bordered condensed hover responsive>
							<thead>
								<tr><th>Track</th><th colSpan="2">Album</th></tr>
							</thead>
							<tbody>
								{this.state.tracks}
							</tbody>
						</Table>
					</div>
				</div>
			</div>
		);
	}
});

export default Artist;
