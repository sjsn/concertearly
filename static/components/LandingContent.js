import React from 'react';

import Search from './Search'

var LandingContent = React.createClass({
	handleSearchChange: function(e) {
		this.props.onSearchChange(e);
	},
	handleSelectChange: function(e) {
		this.props.onSelectChange(e);
	},
	render: function() {
		return (
			<div className="landing-info">	
				<img src="static/logo.png" className="brand" />
				<div className="landing-content">
					<Search 
						onSubmit={this.props.onSubmit} 
						onSearchChange={this.handleSearchChange}
						onSelectChange={this.handleSelectChange}
						context='landing-form'
						/>
					<p><a href="#">Sign in with Spotify.</a></p>
				</div>
			</div>
		);
	}
});

export default LandingContent;