import React from 'react';
import ReactDOM from 'react-dom';

import LandingPage from './components/LandingPage';
import HomePage from './components/HomePage';

import Nav from './components/Nav';
import Body from './components/Body';
import Footer from './components/Footer';

import $ from 'jquery';

var App = React.createClass({
	getInitialState: function() {
		return {page: <LandingPage 
						onSubmit={this.handleSubmit} 
						onSearchChange={this.handleSearchChange}
						onSelectChange={this.handleSelectChange}
						/>,
				search: '',
				method: 'concert'};
	},
	onSearchChange: function(text) {
		this.setState({search: text});
		console.log(this.state.page);
		console.log(this.state.text);
		console.log(this.state.item);
	},
	onSelectChange: function(item) {
		this.setState({method: item});
		console.log(this.state.page);
		console.log(this.state.text);
		console.log(this.state.item);
	},
	handleSubmit: function(e) {
		e.preventDefault();
		console.log();
		this.setState({page: <HomePage 
								onSubmit={this.handleSubmit} 
								onSearchChange={this.handleSearchChange}
								onSelectChange={this.handleSelectChange}
								/>});
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