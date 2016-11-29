import React from 'react';

import Navigation from './Navigation';
import Footer from './Footer';
import HomeContent from './HomeContent';
import DetailPage from './DetailPage';

import $ from 'jquery';

var HomePage = React.createClass({
	getInitialState: function() {
		return ({
			curTerm: this.props.search,
			search: this.props.search,
			method: this.props.method,
			data: {},
			page: ''
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
				this.setState({data: data,
					page: <HomeContent 
							items={data.events} 
							length={data.total}
							term={this.state.curTerm} 
							onClick={this.handleClick}
							/>
				});
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
						method:this.state.method,
						curTerm: this.state.search
						});
		this.handleNewSearch();
	},
	handleClick: function(artists) {
		var newPage = <DetailPage 
						data={artists}
						/>;
		this.setState({page: newPage});
	},
	render: function() {
		return (
			<div>
				<Navigation 
					onSubmit={this.handleSubmit} 
					onSearchChange={this.handleSearchChange}
					onSelectChange={this.handleSelectChange}
					/>
				{this.state.page}
				<Footer />
			</div>
		);
	}
});

export default HomePage;
