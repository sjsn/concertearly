import React from 'react';

import Navigation from './Navigation';
import Footer from './Footer';
import HomeContent from './HomeContent';

import $ from 'jquery';

var HomePage = React.createClass({
	getInitialState: function() {
		return ({
			search: this.props.search,
			method: this.props.method,
			data: {}
		});
	},
	componentWillMount: function() {
		this.handleNewSearch();
	},
	handleNewSearch: function() {
		$.ajax({
			url: '/api/get_events',
			type: 'POST',
			data: {
				search: this.state.search,
				method: this.state.method
			},
			success: function(data) {
				this.setState({data: data})
			}.bind(this),
			error: function(xhr, status, err) {
				console.log(err);
			}
		});
	},
	handleSearchChange: function(e) {
		this.setState({search: e});
	},
	handleSelectChange: function(e) {
		this.setState({method: e});
		if (e == 'artist') {
			this.setState({keyword: 'Search by artist name'});
		} else if (e == 'venue') {
			this.setState({keyword: 'Search by venue name'});
		} else if (e == 'location') {
			this.setState({keyword: 'Search by zipcode'})
		}
	},
	handleSubmit: function(e) {
		e.preventDefault();
		var body = document.querySelector('body');
		body.style.backgroundColor = '#eef0f2';
		this.setState({search: this.state.search,
						method:this.state.method
						});
		this.handleNewSearch();
	},
	render: function() {
		return (
			<div>
				<Navigation 
					onSubmit={this.handleSubmit} 
					onSearchChange={this.handleSearchChange}
					onSelectChange={this.handleSelectChange}
					/>
				<HomeContent 
					items={this.state.data.events} 
					term={this.state.search} />
				<Footer />
			</div>
		);
	}
});

export default HomePage;
