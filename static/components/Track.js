import React from 'react';

import Table from 'react-bootstrap/lib/Table';

var Track = React.createClass({
	render: function() {
		return (
			<tr key={this.props.track.id}>
				<td>{this.props.track.name}</td>
				<td>{this.props.track.album}</td>
				<td><a href={this.props.track.sample} target="_blank"><i className="fa fa-play play-btn"></i></a></td>
			</tr>
		);
	}
});

export default Track;
