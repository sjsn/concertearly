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
	handleClick: function(artists, venue, date, title, url) {
		this.props.onClick(artists, venue, date, title, url);
	},
	changePage: function(key) {
		if (this.props.length) {
			var items = this.props.items.slice((key - 1) * 4, key * 4);
			this.setState({total: items.length});
			var searchResults = items.map(function(item, index) {
				var names = [];
				var artists = item.performers.map(function(artist, index, arr) {
					names.push(artist.name);
					return (
						<span className='artist-res' key={artist.id}>{artist.name}{arr[index + 1] ? ',' : ''} </span>
					);
				});
				var date = new Date(item.datetime_utc);
				date = date.toDateString().split(' ');
				date = date[0] + " " + date[1] + " " + date[2] + ", " + date[3];
				return (
					<Result 
						venueName={item.venue.name}
						venueAddress={item.venue.extended_address}
						eventTitle={item.short_title}
						artists={artists}
						names={names}
						date={date}
						url={item.url + '&aid=12402'}
						key={index}
						onClick={this.handleClick}
					/>
				);
			}.bind(this));
		} else {
			var searchResults = (
				<p className='blank'>
					We couldn't find anything for '{this.props.term}'. Please try again.
				</p>
			);
		}
		return searchResults;
	},
	render: function() {
		return (
			<div className='results'>
				<h2 className="result-head">Showing results for '{this.props.term}'</h2>
				{this.state.searchResults}
				<div className="page-holder">
					<p className="result-count">Showing {this.state.total} out of {this.props.items.length} results</p>
					<Pagination
						prev
						next
						first
						last
						ellipsis
						boundaryLinks
						items={Math.ceil(this.props.items.length / 4)}
						maxButtons={6}
						activePage={this.state.activePage}
						onSelect={this.handleSelect}
						className={this.props.items == null || this.props.items.length <= 5  ? 'hidden page-nums' : 'page-nums'}
					/>
				</div>
			</div>
		);
	}
});

export default HomeContent;
