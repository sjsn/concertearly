import React from 'react';

import Result from './Result';
import DetailPage from './DetailPage';
import Pagination from 'react-bootstrap/lib/Pagination';

var HomeContent = React.createClass({
	getInitialState: function() {
		return {activePage: 1, searchResults: []};
	},
	componentDidMount: function() {
		if (this.props.items) {
			this.setState({searchResults: this.changePage(1)});
		}
	},
	handleSelect: function(eventKey) {
		this.setState({activePage: eventKey, searchResults: this.changePage(eventKey)});
	},
	handleClick: function(artists, venue, date, title) {
		this.props.onClick(artists, venue, date, title);
	},
	changePage: function(key) {
		var items = this.props.items.slice((key - 1) * 5, key * 5);
		var searchResults = items.map(function(item, index) {
			var names = [];
			var artists = item.performers.map(function(artist) {
				names.push(artist.name);
				return (
					<span className='artist-res' key={artist.id}> {artist.name} | </span>
				);
			});
			var date = new Date(item.datetime_utc);
			date = date.toDateString();
			return (
				<Result 
					venueName={item.venue.name}
					venueAddress={item.venue.extended_address}
					eventTitle={item.short_title}
					artists={artists}
					names={names}
					date={date}
					key={index}
					onClick={this.handleClick}
				/>
			);
		}.bind(this));
		return searchResults;
	},
	render: function() {
		if (this.props.items) {
			return (
				<div className='results'>
					<h2>Showing results for '{this.props.term}'</h2>
					{this.state.searchResults}
					<div className="page-holder">
						<Pagination
							prev
							next
							first
							last
							ellipsis
							boundaryLinks
							items={Math.ceil(this.props.items.length / 5)}
							maxButtons={6}
							activePage={this.state.activePage}
							onSelect={this.handleSelect}
							className={this.props.items.length <= 5 ? 'hidden' : ''}
						/>
					</div>
				</div>
			);
		} else {
			return (
				<div>
					<h2 className='result-title'>Showing results for '{this.props.term}'</h2>
					<p className='loading'><i className='fa-spinner'></i></p>
				</div>
			);
		}
	}
});

export default HomeContent;
