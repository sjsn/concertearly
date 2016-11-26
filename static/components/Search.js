import React from 'react';

var Search = React.createClass({
	render: function() {
		return (
			<div className="search-bar">
				<input type="text" placeholder="Search..." />
				<button onClick={this.props.onClick}><i className="fa fa-search"></i></button>
			</div>
		);
	}
});

export default Search;