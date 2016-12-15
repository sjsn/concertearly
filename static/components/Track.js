import React from 'react';

import Table from 'react-bootstrap/lib/Table';

var Track = React.createClass({
	getInitialState: function() {
		return {play: "fa fa-play play-btn"};
	},
	handlePlay: function() {
		this.props.onClick(this.props.track);
		if (this.state.play = "fa fa-play play-btn") {
			this.setState({play: "fa fa-pause pause-btn"});
		} else {
			this.setState({play: "fa fa-play play-btn"});
		}
	},
	render: function() {
		return (
			<tr key={this.props.track.id}>
				<td>{this.props.track.name}</td>
				<td>{this.props.track.album}</td>
				<td><i className={this.state.play} onClick={this.handlePlay}></i></td>
			</tr>
		);
	}
});

export default Track;
