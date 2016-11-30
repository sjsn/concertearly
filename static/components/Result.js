import React from 'react';

var Result = React.createClass({
	handleClick: function() {
		this.props.onClick(this.props.names, this.props.venueName, this.props.date);
	},
	render: function() {
		return (
			<div className='result' onClick={this.handleClick}>
				<p className='date'>
					<span className='title'>Date: </span>
					{this.props.date}
				</p>
				<p className='venue'>
					<span className='title'>Venue: </span> 
					{this.props.venueName}
				</p>
				<p className='loc'>
					<span className='title'>Location: </span> 
					{this.props.venueCity}, {this.props.venueState}, {this.props.venueZip}
				</p>
				<p className='artists'>
					<span className='title'>Artists: </span> 
					{this.props.artists}
				</p>
			</div>
		);
	}
});

export default Result;
