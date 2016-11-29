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
				this.setState({data: data})
			}.bind(this),
			error: function(xhr, status, err) {
				console.log(err);
			}
		});
	},
	render: function() {
		return (
			<h1>{this.props.artists}</h1>
		);
	}
});

export default DetailPage;
