import React from 'react';

import FormGroup from 'react-bootstrap/lib/FormGroup';
import InputGroup from 'react-bootstrap/lib/InputGroup';
import FormControl from 'react-bootstrap/lib/FormControl';
import Button from 'react-bootstrap/lib/Button';

var Search = React.createClass({
	getInitialState: function() {
		return ({
			keyword: 'Search by artist name'
		});
	},
	handleSearchChange: function(e) {
		this.props.onSearchChange(e.target.value);
	},
	handleSelectChange: function(e) {
		this.props.onSelectChange(e.target.value);
		if (e.target.value == 'artist') {
			this.setState({keyword: 'Search by artist name'});
		} else if (e.target.value == 'venue') {
			this.setState({keyword: 'Search by venue name'});
		} else if (e.target.value == 'location') {
			this.setState({keyword: 'Search by zipcode'});
		} else if (e.target.value == 'concert') {
			this.setState({keyword: 'Search by concert name'});
		}
	},
	render: function() {
		return (
			<form className={this.props.context} onSubmit={this.props.onSubmit}>
				<FormGroup>
					<p className={this.props.context == 'landing-form' ? 'search-prompt' : 'hidden'}>Search by: </p>
					<InputGroup className={this.props.context == 'landing-form' ? 'land-select type-select' : 'type-select'}>
						<FormControl 
							componentClass="select" 
							name="method"
							onChange={this.handleSelectChange}>
							<option value="artist">Artist</option>
							<option value="venue">Venue</option>
							<option value="location">Location</option>
							<option value="concert">Concert</option>
						</FormControl>
					</InputGroup>
					<InputGroup>
						<FormControl 
							type="text" 
							placeholder={this.state.keyword}
							name="search" 
							onChange={this.handleSearchChange} />
        				<InputGroup.Button>
        					<Button type="submit"><i className="fa fa-search"></i></Button>
        				</InputGroup.Button>
    				</InputGroup>
				</FormGroup>
			</form>
		);
	}
});

export default Search;
