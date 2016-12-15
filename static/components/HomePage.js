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
			page: (
					<div className='results'>
						<h2 className='result-title'>Showing results for '{this.props.search}'</h2>
						<p className='loading'><i className='fa fa-spinner'></i></p>
					</div>
				) 
		});
	},
	componentWillMount: function() {
		this.handleNewSearch();
	},
	handleNewSearch: function() {
		this.setState({page: <div className='results'>
								<h2 className='result-title'>Showing results for '{this.props.search}'</h2>
								<p className='loading'><i className='fa fa-spinner'></i></p>
							</div>});
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
	handleSearchChange: function(search) {
		this.setState({search: search});
	},
	handleSelectChange: function(method) {
		this.setState({method: method});
		if (method == 'artist') {
			this.setState({keyword: 'Search by artist name'});
		} else if (method == 'venue') {
			this.setState({keyword: 'Search by venue name'});
		} else if (method == 'location') {
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
	handleClick: function(artists, venue, date, title) {
		var newPage = <DetailPage 
						artists={artists}
						venue={venue}
						date={date}
						title={title}
						/>;
		this.setState({page: newPage});
	},
	render: function() {
		return (
			<div className="main-holder">
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
