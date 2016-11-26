import React from 'react';
import Search from './Search'

var Nav = React.createClass({
	handleSearch: function(e) {
		console.log(e);
	},
	render: function() {
		return (
			<nav className="navbar-top">
				<a href="/">
					<img className="nav-logo" src="static/favicon.png" alt="logo" />
				</a>
				<Search onClick={this.handleSearch} />
			</nav>
		);
	}
});

export default Nav;