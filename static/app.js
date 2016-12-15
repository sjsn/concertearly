import React from 'react';
import ReactDOM from 'react-dom';

import { Router, Route, hashHistory } from 'react-router';

import LandingPage from './components/LandingPage';
import HomePage from './components/HomePage';

var App = React.createClass({
	getInitialState: function() {
		return {page: <LandingPage 
						onSubmit={this.handleSubmit} 
						onSearchChange={this.handleSearchChange}
						onSelectChange={this.handleSelectChange}
						/>,
				search: '',
				method: 'artist'};
	},
	handleSearchChange: function(text) {
		this.setState({search: text});
	},
	handleSelectChange: function(item) {
		this.setState({method: item});
	},
	handleSubmit: function(e) {
		e.preventDefault();
		var body = document.querySelector('body');
		body.style.backgroundColor = '#eef0f2';
		body.style.background = 'none';
		// Temporary routing solution. Switch to React-Router later
		if (this.state.search) {
			this.setState({page: <HomePage 
									onSubmit={this.handleSubmit} 
									onSearchChange={this.handleSearchChange}
									onSelectChange={this.handleSelectChange}
									search={this.state.search}
									method={this.state.method}
									/>});
		}
	},
	render: function() {
		return (
			<div>
				{this.state.page}
			</div>
		);
	}
});

ReactDOM.render(
	<App />,
	document.getElementById('content')
);
