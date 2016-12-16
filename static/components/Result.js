import React from 'react';

var Result = React.createClass({
	handleClick: function() {
		this.props.onClick(this.props.names, this.props.venueName, this.props.date, this.props.eventTitle, this.props.url);
	},
	render: function() {
		return (
			<div className='result' onClick={this.handleClick}>
				<p className="concert-title">
					<span className="event-name">{this.props.eventTitle}</span> @ <span className="venue-name">{this.props.venueName}</span>
				</p>
				<p>
					<span className="date">{this.props.date}</span> – <span className="address">{this.props.venueAddress}</span>
				</p>
				<p className="artists">
					Featuring: {this.props.artists}
				</p>
			</div>
		);
	}
});

export default Result;
