import React from 'react';

var Artist = React.createClass({
	getInitialState: function() {
		return {added: true, icon: <i className="fa fa-check-circle-o added-ico"></i>};
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
	render: function() {
		var tracks = this.props.artist.tracks.map(function(track) {
				return (
					<li key={track.id}><a href={track.sample}>{track.name}</a></li>
				);
			});
		return (
			<div key={this.props.artist.id} className="concert-artist">
				<ul className="artist">
					<h3 className='name'>{this.props.artist.name}</h3>
					<button className="add-toggle" onClick={this.handleToggle}>
						{this.state.icon}
					</button>
					<img src={this.props.artist.image} alt={this.props.artist.name} className="artist-img" />
					{tracks}
				</ul>
			</div>
		);
	}
});

export default Artist;
