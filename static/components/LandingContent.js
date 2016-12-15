import React from 'react';

import Search from './Search'
import $ from 'jquery';

var LandingContent = React.createClass({
	getInitialState: function() {
		return {'spot': <p><a href="/spotify/auth">Sign in with Spotify.</a></p>};
	},
	componentDidMount: function() {
		$.ajax({
			url: '/get_user',
			type: 'GET',
			success: function(data) {
				console.log(data)
				this.setState({spot: <p>Signed in as {data.display_name}.</p>});
			}.bind(this),
			error: function(xhr, status, err) {
				console.log(err);
			}
		});
	},
	handleSearchChange: function(e) {
		this.props.onSearchChange(e);
	},
	handleSelectChange: function(e) {
		this.props.onSelectChange(e);
	},
	render: function() {
		return (
			<div className="landing-info">	
				<a href="/"><img src="static/logo.png" className="brand" /></a>
				<div className="landing-content">
					<Search 
						onSubmit={this.props.onSubmit} 
						onSearchChange={this.handleSearchChange}
						onSelectChange={this.handleSelectChange}
						context='landing-form'
						/>
				</div>
				{this.state.spot}
			</div>
		);
	}
});

export default LandingContent;
